"""
Scan management endpoints
"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Site, Page, Issue
from app.schemas import ScanRequest, ScanResponse, ScanStatus, ScanResults
from app.config import settings

router = APIRouter()


# ============================================================================
# Background Task Functions
# ============================================================================

async def crawl_website(scan_id: str, url: str, max_pages: int, max_depth: int):
    """
    Background task to crawl website
    
    This is a placeholder - actual implementation will use Playwright crawler
    """
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Update site status to in_progress
        site = db.query(Site).filter(Site.id == scan_id).first()
        if site:
            site.status = "in_progress"
            site.updated_at = datetime.utcnow()
            db.commit()
        
        # TODO: Implement actual crawling logic
        # from app.crawler.playwright_crawler import crawl_site
        # results = await crawl_site(url, max_pages, max_depth)
        
        # For now, just mark as completed
        if site:
            site.status = "completed"
            site.pages_scanned = 0
            site.total_pages = 0
            site.updated_at = datetime.utcnow()
            db.commit()
            
    except Exception as e:
        # Mark scan as failed
        site = db.query(Site).filter(Site.id == scan_id).first()
        if site:
            site.status = "failed"
            site.error_message = str(e)
            site.updated_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()


# ============================================================================
# Scan Endpoints
# ============================================================================

@router.post("", response_model=ScanResponse, status_code=201)
async def create_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Initiate a new website scan
    
    - **url**: Website URL to scan
    - **max_pages**: Maximum number of pages to scan (default: 50)
    - **max_depth**: Maximum crawl depth (default: 3)
    
    Returns a scan ID that can be used to check status
    """
    # Generate unique scan ID
    scan_id = str(uuid.uuid4())
    
    # Create site record
    site = Site(
        id=scan_id,
        domain_url=str(request.url),
        status="pending",
        created_at=datetime.utcnow()
    )
    
    db.add(site)
    db.commit()
    db.refresh(site)
    
    # Start background crawl task
    background_tasks.add_task(
        crawl_website,
        scan_id,
        str(request.url),
        request.max_pages,
        request.max_depth
    )
    
    return ScanResponse(
        scan_id=scan_id,
        status="pending",
        created_at=site.created_at
    )


@router.get("/{scan_id}", response_model=ScanStatus)
async def get_scan_status(
    scan_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the current status of a scan
    
    Use this endpoint to poll for scan progress
    """
    site = db.query(Site).filter(Site.id == scan_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Calculate progress percentage
    progress = 0
    if site.total_pages > 0:
        progress = int((site.pages_scanned / site.total_pages) * 100)
    elif site.status == "completed":
        progress = 100
    elif site.status == "in_progress":
        progress = 50  # Arbitrary progress for in-progress scans
    
    return ScanStatus(
        scan_id=site.id,
        status=site.status,
        progress=progress,
        pages_scanned=site.pages_scanned,
        total_pages=site.total_pages,
        created_at=site.created_at,
        updated_at=site.updated_at,
        error_message=site.error_message
    )


@router.get("/{scan_id}/results", response_model=ScanResults)
async def get_scan_results(
    scan_id: str,
    db: Session = Depends(get_db)
):
    """
    Get complete scan results
    
    Only available when scan status is 'completed'
    """
    site = db.query(Site).filter(Site.id == scan_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if site.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Scan is not completed yet. Current status: {site.status}"
        )
    
    # Get all pages for this site
    pages = db.query(Page).filter(Page.site_id == scan_id).all()
    
    # Get all issues for this site
    issues = db.query(Issue).join(Page).filter(Page.site_id == scan_id).all()
    
    # Calculate statistics
    issues_by_type = {}
    issues_by_severity = {}
    
    for issue in issues:
        issues_by_type[issue.type] = issues_by_type.get(issue.type, 0) + 1
        issues_by_severity[issue.severity] = issues_by_severity.get(issue.severity, 0) + 1
    
    # Get top 10 issues by priority
    top_issues = sorted(issues, key=lambda x: x.priority_score, reverse=True)[:10]
    
    return ScanResults(
        scan_id=site.id,
        domain_url=site.domain_url,
        status=site.status,
        global_score=site.global_score,
        created_at=site.created_at,
        pages_scanned=site.pages_scanned,
        total_issues=len(issues),
        issues_by_type=issues_by_type,
        issues_by_severity=issues_by_severity,
        top_issues=top_issues,
        pages=pages
    )


@router.delete("/{scan_id}", status_code=204)
async def delete_scan(
    scan_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a scan and all associated data
    
    This will cascade delete all pages, issues, and recommendations
    """
    site = db.query(Site).filter(Site.id == scan_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(site)
    db.commit()
    
    return None

# Made with Bob

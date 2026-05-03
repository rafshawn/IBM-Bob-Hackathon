"""
Issue management endpoints
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dependencies import get_db
from app.models import Issue, Page
from app.schemas import IssueList, IssueDetail, IssuePriority

router = APIRouter()


@router.get("", response_model=IssueList)
async def get_issues(
    scan_id: Optional[str] = Query(None, description="Filter by scan ID"),
    page_id: Optional[str] = Query(None, description="Filter by page ID"),
    issue_type: Optional[str] = Query(None, description="Filter by type (seo, accessibility, qa)"),
    severity: Optional[str] = Query(None, description="Filter by severity (high, medium, low)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of issues with optional filters
    
    - **scan_id**: Filter issues by scan
    - **page_id**: Filter issues by page
    - **type**: Filter by issue type (seo, accessibility, qa)
    - **severity**: Filter by severity (high, medium, low)
    - **page**: Page number for pagination
    - **page_size**: Number of items per page
    """
    query = db.query(Issue).join(Page)
    
    # Apply filters
    if scan_id:
        query = query.filter(Page.site_id == scan_id)
    
    if page_id:
        query = query.filter(Issue.page_id == page_id)
    
    if issue_type:
        query = query.filter(Issue.type == issue_type.lower())
    
    if severity:
        query = query.filter(Issue.severity == severity.lower())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    issues = query.order_by(desc(Issue.priority_score)).offset(offset).limit(page_size).all()
    
    # Add page URL to each issue
    for issue in issues:
        issue.page_url = issue.page.url
    
    return IssueList(
        issues=issues,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/priority", response_model=List[IssuePriority])
async def get_priority_issues(
    scan_id: Optional[str] = Query(None, description="Filter by scan ID"),
    limit: int = Query(10, ge=1, le=50, description="Number of top issues to return"),
    db: Session = Depends(get_db)
):
    """
    Get prioritized issues sorted by priority score
    
    Returns the top issues that should be addressed first
    """
    query = db.query(Issue).join(Page)
    
    if scan_id:
        query = query.filter(Page.site_id == scan_id)
    
    issues = query.order_by(desc(Issue.priority_score)).limit(limit).all()
    
    # Build priority response with impact descriptions
    priority_issues = []
    for issue in issues:
        impact = _get_impact_description(issue.type, issue.severity)
        
        priority_issues.append(IssuePriority(
            id=issue.id,
            type=issue.type,
            severity=issue.severity,
            title=issue.title,
            priority_score=issue.priority_score,
            page_url=issue.page.url,
            impact=impact
        ))
    
    return priority_issues


@router.get("/{issue_id}", response_model=IssueDetail)
async def get_issue(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific issue
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Add page URL
    issue.page_url = issue.page.url
    
    return issue


# ============================================================================
# Helper Functions
# ============================================================================

def _get_impact_description(issue_type: str, severity: str) -> str:
    """
    Generate human-readable impact description
    """
    impact_map = {
        ("accessibility", "high"): "Critical accessibility barrier - prevents users with disabilities from accessing content",
        ("accessibility", "medium"): "Moderate accessibility issue - may cause difficulty for some users",
        ("accessibility", "low"): "Minor accessibility improvement - enhances user experience",
        ("seo", "high"): "Major SEO issue - significantly impacts search rankings and discoverability",
        ("seo", "medium"): "Moderate SEO issue - may reduce search visibility",
        ("seo", "low"): "Minor SEO optimization - small improvement opportunity",
        ("qa", "high"): "Critical quality issue - may break functionality or user experience",
        ("qa", "medium"): "Moderate quality issue - affects user experience",
        ("qa", "low"): "Minor quality improvement - enhances overall quality"
    }
    
    return impact_map.get((issue_type, severity), "Issue requires attention")

# Made with Bob

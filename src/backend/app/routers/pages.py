"""
Page management endpoints
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Page, Issue
from app.schemas import PageList, PageDetail

router = APIRouter()


@router.get("", response_model=PageList)
async def get_pages(
    scan_id: Optional[str] = Query(None, description="Filter by scan ID"),
    page_num: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of scanned pages
    
    - **scan_id**: Filter pages by scan
    - **page**: Page number for pagination
    - **page_size**: Number of items per page
    """
    query = db.query(Page)
    
    if scan_id:
        query = query.filter(Page.site_id == scan_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page_num - 1) * page_size
    pages = query.offset(offset).limit(page_size).all()
    
    return PageList(
        pages=pages,
        total=total,
        page=page_num,
        page_size=page_size
    )


@router.get("/{page_id}", response_model=PageDetail)
async def get_page(
    page_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific page
    
    Includes all issues found on this page
    """
    page = db.query(Page).filter(Page.id == page_id).first()
    
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    return page


@router.get("/{page_id}/issues")
async def get_page_issues(
    page_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all issues for a specific page
    """
    page = db.query(Page).filter(Page.id == page_id).first()
    
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    issues = db.query(Issue).filter(Issue.page_id == page_id).all()
    
    return {
        "page_id": page_id,
        "page_url": page.url,
        "total_issues": len(issues),
        "issues": issues
    }

# Made with Bob

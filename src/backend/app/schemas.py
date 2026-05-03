"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field, validator


# ============================================================================
# Scan Schemas
# ============================================================================

class ScanRequest(BaseModel):
    """Request to start a new website scan"""
    url: HttpUrl
    max_pages: int = Field(default=50, ge=1, le=100, description="Maximum pages to scan")
    max_depth: int = Field(default=3, ge=1, le=5, description="Maximum crawl depth")


class ScanResponse(BaseModel):
    """Response after initiating a scan"""
    scan_id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScanStatus(BaseModel):
    """Current status of a scan"""
    scan_id: str
    status: str  # pending, in_progress, completed, failed
    progress: int = Field(ge=0, le=100, description="Progress percentage")
    pages_scanned: int
    total_pages: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# Page Schemas
# ============================================================================

class PageBase(BaseModel):
    """Base page information"""
    url: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    status_code: Optional[int] = None


class PageDetail(PageBase):
    """Detailed page information"""
    id: str
    site_id: str
    meta_tags: Optional[Dict[str, Any]] = None
    h1_tags: Optional[List[str]] = None
    crawled_at: datetime
    load_time: Optional[float] = None
    
    class Config:
        from_attributes = True


class PageList(BaseModel):
    """List of pages"""
    pages: List[PageDetail]
    total: int
    page: int = 1
    page_size: int = 50


# ============================================================================
# Issue Schemas
# ============================================================================

class IssueBase(BaseModel):
    """Base issue information"""
    type: str  # seo, accessibility, qa
    severity: str  # high, medium, low
    title: str
    description: str
    
    @validator('type')
    def validate_type(cls, v):
        allowed = ['seo', 'accessibility', 'qa']
        if v.lower() not in allowed:
            raise ValueError(f'Type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @validator('severity')
    def validate_severity(cls, v):
        allowed = ['high', 'medium', 'low']
        if v.lower() not in allowed:
            raise ValueError(f'Severity must be one of: {", ".join(allowed)}')
        return v.lower()


class IssueDetail(IssueBase):
    """Detailed issue information"""
    id: str
    page_id: str
    priority_score: int
    snippet: Optional[str] = None
    element_selector: Optional[str] = None
    wcag_criterion: Optional[str] = None
    detected_at: datetime
    page_url: Optional[str] = None  # Populated via join
    
    class Config:
        from_attributes = True


class IssueList(BaseModel):
    """List of issues with pagination"""
    issues: List[IssueDetail]
    total: int
    page: int = 1
    page_size: int = 50


class IssuePriority(BaseModel):
    """Prioritized issue summary"""
    id: str
    type: str
    severity: str
    title: str
    priority_score: int
    page_url: str
    impact: str  # Description of business impact
    
    class Config:
        from_attributes = True


# ============================================================================
# Recommendation Schemas
# ============================================================================

class RecommendationBase(BaseModel):
    """Base recommendation information"""
    suggested_fix_html: str
    ai_explanation: str
    confidence_score: float = Field(ge=0, le=100)
    reasoning: Optional[str] = None


class RecommendationDetail(RecommendationBase):
    """Detailed recommendation"""
    id: str
    issue_id: str
    before_snippet: Optional[str] = None
    after_snippet: Optional[str] = None
    diff_html: Optional[str] = None
    created_at: datetime
    model_used: Optional[str] = None
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    """Request to generate a recommendation"""
    issue_id: str
    force_regenerate: bool = False


# ============================================================================
# Scan Results Schema
# ============================================================================

class ScanResults(BaseModel):
    """Complete scan results"""
    scan_id: str
    domain_url: str
    status: str
    global_score: Optional[float] = None
    created_at: datetime
    pages_scanned: int
    total_issues: int
    issues_by_type: Dict[str, int]
    issues_by_severity: Dict[str, int]
    top_issues: List[IssueDetail]
    pages: List[PageDetail]
    
    class Config:
        from_attributes = True


# ============================================================================
# Health Check Schema
# ============================================================================

class HealthCheck(BaseModel):
    """API health check response"""
    status: str
    version: str
    timestamp: datetime
    database: str
    features: Dict[str, bool]


# ============================================================================
# Error Schema
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Made with Bob

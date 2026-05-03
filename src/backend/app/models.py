"""
Database models for PublicPulse AI
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Site(Base):
    """
    Represents a website scan session
    """
    __tablename__ = "sites"
    
    id = Column(String, primary_key=True)  # UUID
    domain_url = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="pending", nullable=False)  # pending, in_progress, completed, failed
    global_score = Column(Float, nullable=True)
    total_pages = Column(Integer, default=0)
    pages_scanned = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    pages = relationship("Page", back_populates="site", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Site(id={self.id}, domain={self.domain_url}, status={self.status})>"


class Page(Base):
    """
    Represents an individual page within a scanned site
    """
    __tablename__ = "pages"
    
    id = Column(String, primary_key=True)  # UUID
    site_id = Column(String, ForeignKey("sites.id"), nullable=False, index=True)
    url = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_tags = Column(JSON, nullable=True)  # Store as JSON
    h1_tags = Column(JSON, nullable=True)  # List of H1 tags
    crawled_at = Column(DateTime, default=datetime.utcnow)
    status_code = Column(Integer, nullable=True)
    load_time = Column(Float, nullable=True)  # in seconds
    
    # Relationships
    site = relationship("Site", back_populates="pages")
    issues = relationship("Issue", back_populates="page", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Page(id={self.id}, url={self.url})>"


class Issue(Base):
    """
    Represents a detected issue on a page
    """
    __tablename__ = "issues"
    
    id = Column(String, primary_key=True)  # UUID
    page_id = Column(String, ForeignKey("pages.id"), nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # seo, accessibility, qa
    severity = Column(String, nullable=False, index=True)  # high, medium, low
    priority_score = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    snippet = Column(Text, nullable=True)  # HTML snippet showing the issue
    element_selector = Column(String, nullable=True)  # CSS selector for the element
    wcag_criterion = Column(String, nullable=True)  # e.g., "1.1.1", "2.4.6"
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    page = relationship("Page", back_populates="issues")
    recommendations = relationship("Recommendation", back_populates="issue", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Issue(id={self.id}, type={self.type}, severity={self.severity})>"


class Recommendation(Base):
    """
    Represents an AI-generated recommendation for fixing an issue
    """
    __tablename__ = "recommendations"
    
    id = Column(String, primary_key=True)  # UUID
    issue_id = Column(String, ForeignKey("issues.id"), nullable=False, index=True)
    suggested_fix_html = Column(Text, nullable=False)
    ai_explanation = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0-100
    reasoning = Column(Text, nullable=True)
    before_snippet = Column(Text, nullable=True)
    after_snippet = Column(Text, nullable=True)
    diff_html = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String, nullable=True)  # e.g., "watsonx-llama-2-70b"
    
    # Relationships
    issue = relationship("Issue", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, confidence={self.confidence_score})>"

# Made with Bob

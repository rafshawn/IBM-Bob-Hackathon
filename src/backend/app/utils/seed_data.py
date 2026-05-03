"""
Seed data for demo and testing purposes

This module provides realistic mock issues that can be used when:
1. The crawler fails (e.g., Playwright crashes)
2. Testing the recommendation system
3. Demonstrating the product without a live crawl

The seeded issues are designed to:
- Cover common accessibility and SEO problems
- Have realistic HTML snippets
- Work with the existing recommendation system
- Provide a complete demo path: scan → issues → recommendations → frontend
"""
import uuid
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from app.models import Site, Page, Issue
from app.utils.priority_scoring import calculate_priority_score


def seed_demo_issues(db: Session, scan_id: str, base_url: str) -> int:
    """
    Seed the database with realistic demo issues
    
    This function creates a complete demo dataset including:
    - A homepage with multiple issues
    - Realistic HTML snippets
    - Proper WCAG criteria
    - Varied severity levels
    
    Args:
        db: Database session
        scan_id: UUID of the scan/site
        base_url: Base URL of the site being scanned
        
    Returns:
        Number of issues created
    """
    # Create a demo page (homepage)
    page_id = str(uuid.uuid4())
    page = Page(
        id=page_id,
        site_id=scan_id,
        url=base_url,
        title="Home - Example Government Website",
        meta_description=None,  # Will trigger missing meta description issue
        meta_tags={},
        h1_tags=["Welcome", "About Us"],  # Multiple H1s - will trigger issue
        crawled_at=datetime.utcnow(),
        status_code=200
    )
    db.add(page)
    db.flush()
    
    issues = []
    
    # Issue 1: Missing Alt Text (High Priority Accessibility)
    issues.append(Issue(
        id=str(uuid.uuid4()),
        page_id=page_id,
        type='accessibility',
        severity='high',
        priority_score=calculate_priority_score(
            issue_type='accessibility',
            severity='high',
            page_url=base_url,
            element_count=3
        ),
        title='Missing Alt Text on 3 Images',
        description='This page has 3 images without alt text. Alt text is essential for screen reader users to understand image content. All images should have descriptive alt attributes.',
        snippet='<img src="/hero-image.jpg" alt="">\n<img src="/icon-services.png">\n<img src="/photo-team.jpg" alt="">',
        element_selector='img:not([alt]), img[alt=""]',
        wcag_criterion='1.1.1'  # Non-text Content
    ))
    
    # Issue 2: Missing Meta Description (Medium Priority SEO)
    issues.append(Issue(
        id=str(uuid.uuid4()),
        page_id=page_id,
        type='seo',
        severity='medium',
        priority_score=calculate_priority_score(
            issue_type='seo',
            severity='medium',
            page_url=base_url
        ),
        title='Missing Meta Description',
        description='This page does not have a meta description. Meta descriptions appear in search results and help users understand what your page is about. They should be 150-160 characters long.',
        snippet='<head>\n  <title>Home - Example Government Website</title>\n  <!-- Missing <meta name="description" content="..."> -->\n</head>',
        element_selector='head > meta[name="description"]',
        wcag_criterion=None
    ))
    
    # Issue 3: Multiple H1 Headings (Medium Priority SEO)
    issues.append(Issue(
        id=str(uuid.uuid4()),
        page_id=page_id,
        type='seo',
        severity='medium',
        priority_score=calculate_priority_score(
            issue_type='seo',
            severity='medium',
            page_url=base_url,
            element_count=2
        ),
        title='Multiple H1 Headings',
        description='This page has 2 H1 headings. Best practice is to have exactly one H1 per page to clearly indicate the main topic.',
        snippet='<h1>Welcome</h1>\n<h1>About Us</h1>',
        element_selector='h1',
        wcag_criterion='2.4.6'  # Headings and Labels
    ))
    
    # Issue 4: Form Input Missing Label (High Priority Accessibility)
    issues.append(Issue(
        id=str(uuid.uuid4()),
        page_id=page_id,
        type='accessibility',
        severity='high',
        priority_score=calculate_priority_score(
            issue_type='accessibility',
            severity='high',
            page_url=base_url,
            element_count=2
        ),
        title='Form Inputs Missing Labels',
        description='This page has 2 form inputs without associated labels. Labels are essential for screen reader users to understand what information to enter.',
        snippet='<form>\n  <input type="text" name="search" placeholder="Search...">\n  <input type="email" name="email" placeholder="Email address">\n  <button type="submit">Submit</button>\n</form>',
        element_selector='input:not([aria-label]):not([id])',
        wcag_criterion='3.3.2'  # Labels or Instructions
    ))
    
    # Issue 5: Low Color Contrast (Medium Priority Accessibility)
    issues.append(Issue(
        id=str(uuid.uuid4()),
        page_id=page_id,
        type='accessibility',
        severity='medium',
        priority_score=calculate_priority_score(
            issue_type='accessibility',
            severity='medium',
            page_url=base_url,
            element_count=1
        ),
        title='Insufficient Color Contrast',
        description='Text on this page has insufficient color contrast (3.2:1). WCAG requires a contrast ratio of at least 4.5:1 for normal text to ensure readability for users with low vision.',
        snippet='<p style="color: #777; background: #fff;">Important information about our services</p>',
        element_selector='p',
        wcag_criterion='1.4.3'  # Contrast (Minimum)
    ))
    
    # Add all issues to database
    for issue in issues:
        db.add(issue)
    
    db.commit()
    
    print(f"✅ Seeded {len(issues)} demo issues for scan {scan_id}")
    
    return len(issues)


def create_demo_scan(db: Session, base_url: str) -> str:
    """
    Create a complete demo scan with seeded issues
    
    This is useful for testing the full workflow without running a real crawl.
    
    Args:
        db: Database session
        base_url: Base URL for the demo scan
        
    Returns:
        Scan ID (UUID)
    """
    # Create site record
    scan_id = str(uuid.uuid4())
    site = Site(
        id=scan_id,
        domain_url=base_url,
        status="completed",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        total_pages=1,
        pages_scanned=1,
        global_score=72.5  # Calculated based on seeded issues
    )
    db.add(site)
    db.commit()
    
    # Seed issues
    issue_count = seed_demo_issues(db, scan_id, base_url)
    
    print(f"✅ Created demo scan {scan_id} with {issue_count} issues")
    
    return scan_id


# Made with Bob
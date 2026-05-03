"""
SEO issue analyzer

Detects SEO-related issues from crawled page data:
- Missing or empty page titles
- Missing or duplicate H1 tags
- Missing meta descriptions
"""
import uuid
from typing import List, Dict, Any
from app.models import Issue
from app.utils.priority_scoring import calculate_priority_score


def analyze_seo_issues(page_id: str, page_data: Dict[str, Any]) -> List[Issue]:
    """
    Analyze a page for SEO issues
    
    Args:
        page_id: UUID of the page record
        page_data: Dictionary containing page data from crawler
    
    Returns:
        List of Issue model instances
    """
    issues = []
    page_url = page_data.get('url', '')
    
    # Check for missing or empty title
    title_issue = check_missing_title(page_id, page_url, page_data)
    if title_issue:
        issues.append(title_issue)
    
    # Check for H1 tag issues
    h1_issues = check_h1_tags(page_id, page_url, page_data)
    issues.extend(h1_issues)
    
    # Check for missing meta description
    meta_desc_issue = check_missing_meta_description(page_id, page_url, page_data)
    if meta_desc_issue:
        issues.append(meta_desc_issue)
    
    return issues


def check_missing_title(page_id: str, page_url: str, page_data: Dict[str, Any]) -> Issue:
    """
    Check if page title is missing or empty
    
    Returns:
        Issue instance if title is missing, None otherwise
    """
    title = page_data.get('title', '').strip()
    
    if not title:
        priority_score = calculate_priority_score(
            issue_type='seo',
            severity='high',
            page_url=page_url
        )
        
        return Issue(
            id=str(uuid.uuid4()),
            page_id=page_id,
            type='seo',
            severity='high',
            priority_score=priority_score,
            title='Missing Page Title',
            description='This page does not have a title tag. Page titles are crucial for SEO and appear in search results. Every page should have a unique, descriptive title.',
            snippet=f'<head>\n  <!-- Missing <title> tag -->\n</head>',
            element_selector='head > title',
            wcag_criterion=None
        )
    
    return None


def check_h1_tags(page_id: str, page_url: str, page_data: Dict[str, Any]) -> List[Issue]:
    """
    Check for H1 tag issues (missing or multiple H1s)
    
    Returns:
        List of Issue instances
    """
    issues = []
    h1_tags = page_data.get('h1_tags', [])
    
    # Check for missing H1
    if not h1_tags or len(h1_tags) == 0:
        priority_score = calculate_priority_score(
            issue_type='seo',
            severity='high',
            page_url=page_url
        )
        
        issues.append(Issue(
            id=str(uuid.uuid4()),
            page_id=page_id,
            type='seo',
            severity='high',
            priority_score=priority_score,
            title='Missing H1 Heading',
            description='This page does not have an H1 heading. H1 tags help search engines understand the main topic of your page and improve accessibility for screen reader users.',
            snippet='<!-- No <h1> tag found on this page -->',
            element_selector='h1',
            wcag_criterion='2.4.6'  # Headings and Labels
        ))
    
    # Check for multiple H1s
    elif len(h1_tags) > 1:
        priority_score = calculate_priority_score(
            issue_type='seo',
            severity='medium',
            page_url=page_url,
            element_count=len(h1_tags)
        )
        
        h1_list = '\n'.join([f'  <h1>{h1}</h1>' for h1 in h1_tags[:3]])  # Show first 3
        if len(h1_tags) > 3:
            h1_list += f'\n  <!-- ... and {len(h1_tags) - 3} more -->'
        
        issues.append(Issue(
            id=str(uuid.uuid4()),
            page_id=page_id,
            type='seo',
            severity='medium',
            priority_score=priority_score,
            title='Multiple H1 Headings',
            description=f'This page has {len(h1_tags)} H1 headings. Best practice is to have exactly one H1 per page to clearly indicate the main topic.',
            snippet=h1_list,
            element_selector='h1',
            wcag_criterion='2.4.6'  # Headings and Labels
        ))
    
    return issues


def check_missing_meta_description(page_id: str, page_url: str, page_data: Dict[str, Any]) -> Issue:
    """
    Check if meta description is missing or empty
    
    Returns:
        Issue instance if meta description is missing, None otherwise
    """
    meta_description = page_data.get('meta_description', '').strip()
    
    if not meta_description:
        priority_score = calculate_priority_score(
            issue_type='seo',
            severity='medium',
            page_url=page_url
        )
        
        return Issue(
            id=str(uuid.uuid4()),
            page_id=page_id,
            type='seo',
            severity='medium',
            priority_score=priority_score,
            title='Missing Meta Description',
            description='This page does not have a meta description. Meta descriptions appear in search results and help users understand what your page is about. They should be 150-160 characters long.',
            snippet='<head>\n  <!-- Missing <meta name="description" content="..."> -->\n</head>',
            element_selector='head > meta[name="description"]',
            wcag_criterion=None
        )
    
    return None


# Made with Bob
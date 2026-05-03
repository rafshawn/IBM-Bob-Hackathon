"""
Accessibility (A11y) issue analyzer

Detects accessibility-related issues from crawled page data:
- Images missing alt text
- Elements missing aria-label
"""
import uuid
from typing import List, Dict, Any, Optional
from app.models import Issue
from app.utils.priority_scoring import calculate_priority_score


def analyze_accessibility_issues(page_id: str, page_data: Dict[str, Any]) -> List[Issue]:
    """
    Analyze a page for accessibility issues
    
    Args:
        page_id: UUID of the page record
        page_data: Dictionary containing page data from crawler
    
    Returns:
        List of Issue model instances
    """
    issues = []
    page_url = page_data.get('url', '')
    
    # Check for images missing alt text
    alt_text_issues = check_missing_alt_text(page_id, page_url, page_data)
    issues.extend(alt_text_issues)
    
    # Check for elements missing aria-label
    aria_issues = check_missing_aria_labels(page_id, page_url, page_data)
    issues.extend(aria_issues)
    
    return issues


def check_missing_alt_text(page_id: str, page_url: str, page_data: Dict[str, Any]) -> List[Issue]:
    """
    Check for images missing alt text
    
    Returns:
        List of Issue instances for images without alt text
    """
    issues = []
    images = page_data.get('images', [])
    
    # Find images without alt text
    images_without_alt = [img for img in images if not img.get('has_alt', False)]
    
    if images_without_alt:
        # Create a single issue for all images missing alt text
        count = len(images_without_alt)
        
        priority_score = calculate_priority_score(
            issue_type='accessibility',
            severity='high',
            page_url=page_url,
            element_count=count
        )
        
        # Build snippet showing examples
        snippet_lines = []
        for img in images_without_alt[:3]:  # Show first 3 examples
            src = img.get('src', 'unknown')
            snippet_lines.append(f'<img src="{src}" alt="">')
        
        if count > 3:
            snippet_lines.append(f'<!-- ... and {count - 3} more images without alt text -->')
        
        snippet = '\n'.join(snippet_lines)
        
        issues.append(Issue(
            id=str(uuid.uuid4()),
            page_id=page_id,
            type='accessibility',
            severity='high',
            priority_score=priority_score,
            title=f'Missing Alt Text on {count} Image{"s" if count > 1 else ""}',
            description=f'This page has {count} image{"s" if count > 1 else ""} without alt text. Alt text is essential for screen reader users to understand image content. All images should have descriptive alt attributes.',
            snippet=snippet,
            element_selector='img:not([alt]), img[alt=""]',
            wcag_criterion='1.1.1'  # Non-text Content
        ))
    
    return issues


def check_missing_aria_labels(page_id: str, page_url: str, page_data: Dict[str, Any]) -> List[Issue]:
    """
    Check for interactive elements that might need aria-labels
    
    Note: This is a basic check. The crawler extracts elements that HAVE aria-labels.
    We can infer issues if we find buttons/links without text content.
    
    Returns:
        List of Issue instances
    """
    issues = []
    
    # This is a placeholder for more sophisticated aria-label checking
    # In a full implementation, we would:
    # 1. Check for buttons without text or aria-label
    # 2. Check for links without text or aria-label
    # 3. Check for form inputs without labels
    # 4. Check for custom interactive elements without proper ARIA
    
    # For MVP, we'll create a general issue if we detect potential problems
    # This would require more detailed DOM analysis in the crawler
    
    # TODO: Enhance crawler to detect interactive elements without labels
    # For now, we'll skip this check and focus on alt text which is more straightforward
    
    return issues


# Made with Bob
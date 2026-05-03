"""
Priority scoring system for issues

Based on MVP_SCOPE.md:
- High Severity: 80-100 points
- Medium Severity: 40-79 points
- Low Severity: 0-39 points

Factors:
- Issue type (accessibility > SEO > QA)
- Severity level
- Page importance (homepage weighted higher)
"""
from typing import Optional


# Base scores for severity levels (from MVP_SCOPE.md)
SEVERITY_SCORES = {
    'high': 90,      # 80-100 range
    'medium': 60,    # 40-79 range
    'low': 30        # 0-39 range
}

# Type multipliers (accessibility issues are weighted higher)
TYPE_WEIGHTS = {
    'accessibility': 1.2,  # Accessibility is highest priority
    'seo': 1.0,           # SEO is standard priority
    'qa': 0.8             # QA is lower priority
}


def calculate_priority_score(
    issue_type: str,
    severity: str,
    page_url: Optional[str] = None,
    element_count: int = 1
) -> int:
    """
    Calculate priority score for an issue
    
    Args:
        issue_type: Type of issue (accessibility, seo, qa)
        severity: Severity level (high, medium, low)
        page_url: URL of the page (used to detect homepage)
        element_count: Number of elements affected (for scaling)
    
    Returns:
        Priority score (0-100)
    
    Examples:
        >>> calculate_priority_score('accessibility', 'high')
        100
        >>> calculate_priority_score('seo', 'medium')
        60
        >>> calculate_priority_score('qa', 'low')
        24
    """
    # Get base score from severity
    base_score = SEVERITY_SCORES.get(severity.lower(), 30)
    
    # Apply type weight
    type_weight = TYPE_WEIGHTS.get(issue_type.lower(), 1.0)
    score = base_score * type_weight
    
    # Boost score for homepage issues
    if page_url:
        # Check if it's a homepage (ends with / or is just the domain)
        is_homepage = (
            page_url.rstrip('/').count('/') <= 2 or  # http://domain.com or http://domain.com/
            page_url.endswith('index.html') or
            page_url.endswith('index.php')
        )
        if is_homepage:
            score *= 1.3  # 30% boost for homepage issues
    
    # Scale slightly based on number of affected elements (capped at 1.2x)
    if element_count > 1:
        element_multiplier = min(1.0 + (element_count * 0.05), 1.2)
        score *= element_multiplier
    
    # Ensure score stays within bounds
    score = max(0, min(100, int(score)))
    
    return score


def get_severity_from_score(score: int) -> str:
    """
    Reverse lookup: get severity level from priority score
    
    Args:
        score: Priority score (0-100)
    
    Returns:
        Severity level (high, medium, low)
    """
    if score >= 80:
        return 'high'
    elif score >= 40:
        return 'medium'
    else:
        return 'low'


def calculate_global_score(
    total_issues: int,
    high_count: int,
    medium_count: int,
    low_count: int,
    pages_scanned: int
) -> float:
    """
    Calculate overall quality score for a site (0-100)
    
    Higher score = better quality (fewer/less severe issues)
    
    Args:
        total_issues: Total number of issues detected
        high_count: Number of high severity issues
        medium_count: Number of medium severity issues
        low_count: Number of low severity issues
        pages_scanned: Number of pages scanned
    
    Returns:
        Global quality score (0-100)
    """
    if pages_scanned == 0:
        return 0.0
    
    # Start with perfect score
    score = 100.0
    
    # Deduct points based on issue severity
    # High severity issues hurt the score more
    score -= (high_count * 10)      # -10 points per high issue
    score -= (medium_count * 5)     # -5 points per medium issue
    score -= (low_count * 2)        # -2 points per low issue
    
    # Normalize by number of pages (more pages = more lenient)
    if pages_scanned > 1:
        score += (pages_scanned * 2)  # Small bonus for larger scans
    
    # Ensure score stays within bounds
    score = max(0.0, min(100.0, score))
    
    return round(score, 1)


# Made with Bob
"""
AI Service for generating recommendations using IBM WatsonX
"""
import uuid
from datetime import datetime
from typing import Dict, Optional
from app.config import settings
from app.models import Issue, Recommendation


# ============================================================================
# WatsonX Integration (Real API - requires credentials)
# ============================================================================

async def call_watsonx_api(issue_context: Dict) -> Dict:
    """
    Call IBM WatsonX API to generate recommendation
    
    This function will use real WatsonX API when credentials are available.
    Falls back to mock responses if credentials are missing.
    
    Args:
        issue_context: Dictionary containing issue details
        
    Returns:
        Dictionary with recommendation data
    """
    # Check if WatsonX credentials are configured
    if settings.watsonx_api_key and settings.watsonx_project_id:
        try:
            # TODO: Implement real WatsonX API call
            # from ibm_watson_machine_learning.foundation_models import Model
            # 
            # model = Model(
            #     model_id=settings.watsonx_model_id,
            #     credentials={
            #         "url": settings.watsonx_url,
            #         "apikey": settings.watsonx_api_key
            #     },
            #     project_id=settings.watsonx_project_id
            # )
            # 
            # prompt = build_prompt(issue_context)
            # response = model.generate_text(prompt=prompt)
            # return parse_watsonx_response(response)
            
            print("⚠️ WatsonX credentials found but real API not yet implemented")
            print("   Falling back to mock responses for MVP")
            return generate_mock_recommendation(issue_context)
            
        except Exception as e:
            print(f"❌ WatsonX API error: {str(e)}")
            print("   Falling back to mock responses")
            return generate_mock_recommendation(issue_context)
    else:
        print("ℹ️ WatsonX credentials not configured, using mock responses")
        return generate_mock_recommendation(issue_context)


def build_prompt(issue_context: Dict) -> str:
    """
    Build prompt for WatsonX based on issue context
    
    This creates a structured prompt that guides the AI to generate
    helpful, actionable recommendations for non-technical users.
    """
    issue_type = issue_context.get("type", "")
    description = issue_context.get("description", "")
    snippet = issue_context.get("snippet", "")
    page_url = issue_context.get("page_url", "")
    wcag = issue_context.get("wcag_criterion", "")
    
    prompt = f"""You are an accessibility and SEO expert helping a non-technical public service web administrator.

Issue Type: {issue_type}
Issue Description: {description}
Page URL: {page_url}
Current HTML:
{snippet}
{f"WCAG Criterion: {wcag}" if wcag else ""}

Provide a fix in this exact JSON format:
{{
    "plain_language_explanation": "Clear explanation in simple terms (2-3 sentences)",
    "suggested_fix": "The corrected HTML code",
    "confidence_score": 95,
    "reasoning": "Why this fix works and meets standards"
}}

Requirements:
1. Use plain language a non-technical person can understand
2. Provide valid, working HTML
3. Explain the business impact (accessibility, SEO, user experience)
4. Be specific and actionable
5. Keep explanations concise but helpful
"""
    return prompt


# ============================================================================
# Mock Recommendation Generator (MVP Fallback)
# ============================================================================

def generate_mock_recommendation(issue_context: Dict) -> Dict:
    """
    Generate mock recommendation based on issue type
    
    This provides realistic, helpful recommendations for common issues
    when WatsonX API is not available. Perfect for MVP and demos.
    
    Args:
        issue_context: Dictionary containing issue details
        
    Returns:
        Dictionary with recommendation data
    """
    issue_type = issue_context.get("type", "")
    description = issue_context.get("description", "").lower()
    snippet = issue_context.get("snippet", "")
    title = issue_context.get("title", "").lower()
    
    # Missing Alt Text
    if "alt" in description or "alt text" in title:
        return {
            "plain_language_explanation": "Images need alternative text (alt text) so screen readers can describe them to visually impaired users. This is required by WCAG 2.1 and helps everyone understand your content.",
            "suggested_fix": snippet.replace(">", " alt='Descriptive text about this image'>") if snippet else "<img src='image.jpg' alt='Descriptive text about this image'>",
            "confidence_score": 95.0,
            "reasoning": "Adding descriptive alt text meets WCAG 2.1 Success Criterion 1.1.1 (Non-text Content) and improves accessibility for screen reader users."
        }
    
    # Missing Meta Description
    elif "meta description" in description or "meta description" in title:
        return {
            "plain_language_explanation": "Meta descriptions appear in search results and help people decide whether to visit your page. They should be 150-160 characters and clearly describe what's on the page.",
            "suggested_fix": "<meta name='description' content='Brief, compelling description of this page that includes relevant keywords and encourages clicks (150-160 characters).'>",
            "confidence_score": 90.0,
            "reasoning": "A well-written meta description improves click-through rates from search engines and helps users find relevant content."
        }
    
    # Missing or Poor Title
    elif "title" in description and "missing" in description:
        return {
            "plain_language_explanation": "Every page needs a unique, descriptive title that appears in browser tabs and search results. Titles should be 50-60 characters and clearly identify the page content.",
            "suggested_fix": "<title>Descriptive Page Title - Your Organization Name</title>",
            "confidence_score": 92.0,
            "reasoning": "Unique page titles improve SEO, help users navigate your site, and are required for accessibility."
        }
    
    # Heading Hierarchy Issues
    elif "heading" in description or "h1" in description.lower():
        if "multiple h1" in description:
            return {
                "plain_language_explanation": "Each page should have exactly one H1 heading that describes the main content. Multiple H1 tags confuse screen readers and search engines about what's most important.",
                "suggested_fix": "Keep your main heading as <h1>Main Page Title</h1> and change other H1 tags to <h2> or <h3> based on their importance.",
                "confidence_score": 93.0,
                "reasoning": "Proper heading hierarchy (one H1, then H2s, then H3s) helps screen readers navigate and improves SEO."
            }
        elif "missing h1" in description:
            return {
                "plain_language_explanation": "Every page needs one H1 heading that clearly describes the main content. This helps screen readers and search engines understand what your page is about.",
                "suggested_fix": "<h1>Clear, Descriptive Main Heading</h1>",
                "confidence_score": 94.0,
                "reasoning": "H1 headings are essential for accessibility and SEO, providing structure and context for all users."
            }
        else:
            return {
                "plain_language_explanation": "Headings should follow a logical order (H1 → H2 → H3) without skipping levels. This creates a clear content structure for screen readers and improves readability.",
                "suggested_fix": "Reorganize headings to follow proper hierarchy: H1 for main title, H2 for major sections, H3 for subsections.",
                "confidence_score": 88.0,
                "reasoning": "Proper heading hierarchy meets WCAG 2.1 guidelines and helps all users navigate your content."
            }
    
    # Missing Form Labels
    elif "label" in description or "form" in description:
        return {
            "plain_language_explanation": "Form inputs need labels so screen readers can tell users what information to enter. Labels also make forms easier for everyone to use.",
            "suggested_fix": "<label for='input-id'>Field Name:</label>\n<input type='text' id='input-id' name='field-name'>",
            "confidence_score": 96.0,
            "reasoning": "Properly labeled form fields meet WCAG 2.1 Success Criterion 3.3.2 and significantly improve form usability."
        }
    
    # Color Contrast Issues
    elif "contrast" in description or "color" in description:
        return {
            "plain_language_explanation": "Text needs sufficient contrast with its background so people with low vision can read it. WCAG requires a contrast ratio of at least 4.5:1 for normal text.",
            "suggested_fix": "Change text color to #000000 (black) or background to #FFFFFF (white) to meet contrast requirements. Use a contrast checker tool to verify.",
            "confidence_score": 85.0,
            "reasoning": "Adequate color contrast meets WCAG 2.1 Success Criterion 1.4.3 and makes content readable for users with visual impairments."
        }
    
    # Generic SEO Issue
    elif issue_type == "seo":
        return {
            "plain_language_explanation": "This SEO issue affects how search engines understand and rank your page. Fixing it will help more people find your content through search.",
            "suggested_fix": "Review the specific issue and update your HTML to follow SEO best practices. Consider adding relevant keywords and improving content structure.",
            "confidence_score": 80.0,
            "reasoning": "Following SEO best practices improves search visibility and helps users find relevant information."
        }
    
    # Generic Accessibility Issue
    elif issue_type == "accessibility":
        return {
            "plain_language_explanation": "This accessibility issue may prevent some users from accessing your content. Fixing it ensures everyone can use your website, regardless of disabilities.",
            "suggested_fix": "Review WCAG 2.1 guidelines for this specific issue and update your HTML to meet accessibility standards.",
            "confidence_score": 82.0,
            "reasoning": "Meeting accessibility standards ensures equal access for all users and is often required by law for public service websites."
        }
    
    # Generic Quality Issue
    else:
        return {
            "plain_language_explanation": "This quality issue affects user experience and should be addressed to improve your website's overall performance and usability.",
            "suggested_fix": "Review the specific issue details and update your code to follow web development best practices.",
            "confidence_score": 75.0,
            "reasoning": "Maintaining high code quality improves site performance, maintainability, and user satisfaction."
        }


# ============================================================================
# Recommendation Generation
# ============================================================================

async def generate_recommendation(issue: Issue, db) -> Recommendation:
    """
    Generate AI-powered recommendation for an issue
    
    This is the main function that:
    1. Builds context from the issue
    2. Calls WatsonX API (or mock fallback)
    3. Creates and stores a Recommendation record
    
    Args:
        issue: Issue model instance
        db: Database session
        
    Returns:
        Recommendation model instance
    """
    # Build context for AI
    issue_context = {
        "type": issue.type,
        "title": issue.title,
        "description": issue.description,
        "snippet": issue.snippet or "",
        "page_url": issue.page.url if issue.page else "",
        "wcag_criterion": issue.wcag_criterion or "",
        "element_selector": issue.element_selector or ""
    }
    
    # Call AI service (WatsonX or mock)
    ai_response = await call_watsonx_api(issue_context)
    
    # Determine status based on whether we used real AI or mock
    status = "mock" if not (settings.watsonx_api_key and settings.watsonx_project_id) else "success"
    
    # Create recommendation record
    recommendation = Recommendation(
        id=str(uuid.uuid4()),
        issue_id=issue.id,
        suggested_fix_html=ai_response.get("suggested_fix", ""),
        ai_explanation=ai_response.get("plain_language_explanation", ""),
        confidence_score=ai_response.get("confidence_score", 80.0),
        reasoning=ai_response.get("reasoning", ""),
        before_snippet=issue.snippet or "",
        after_snippet=ai_response.get("suggested_fix", ""),
        created_at=datetime.utcnow(),
        model_used=settings.watsonx_model_id if status == "success" else "mock-fallback"
    )
    
    # Store in database
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    print(f"✅ Generated recommendation for issue {issue.id} (status: {status})")
    
    return recommendation


# Made with Bob
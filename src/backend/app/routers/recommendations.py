"""
Recommendation endpoints for AI-powered fix suggestions
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Issue, Recommendation
from app.services.ai_service import generate_recommendation
from pydantic import BaseModel

router = APIRouter()


# ============================================================================
# Response Schema (Frontend-Friendly Format)
# ============================================================================

class RecommendationResponse(BaseModel):
    """
    Frontend-friendly recommendation response
    
    This schema matches the expected format from the product requirements:
    - Simple, flat structure
    - Plain language explanation
    - Before/after snippets
    - Confidence score
    - Status indicator (success/mock/error)
    """
    issue_id: str
    issue_type: str
    title: str
    plain_language_explanation: str
    suggested_fix: str
    before_snippet: str
    after_snippet: str
    confidence_score: float
    model_used: str
    status: str  # "success" | "mock" | "error"
    
    class Config:
        from_attributes = True


# ============================================================================
# Recommendation Endpoints
# ============================================================================

@router.get("/{issue_id}", response_model=RecommendationResponse)
async def get_recommendation(
    issue_id: str,
    force_regenerate: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get or generate AI recommendation for an issue
    
    This endpoint:
    1. Looks up the issue by ID
    2. Checks if a recommendation already exists
    3. If not (or force_regenerate=True), generates a new one using AI
    4. Returns the recommendation in a frontend-friendly format
    
    **Parameters:**
    - **issue_id**: UUID of the issue to get recommendation for
    - **force_regenerate**: If true, generates a new recommendation even if one exists
    
    **Returns:**
    - Recommendation with plain-language explanation and suggested fix
    - Status indicates if using real AI ("success") or mock fallback ("mock")
    
    **Example:**
    ```
    GET /api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    # Get the issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=404,
            detail=f"Issue not found with ID: {issue_id}"
        )
    
    # Check for existing recommendation
    existing_rec = None
    if not force_regenerate:
        existing_rec = db.query(Recommendation).filter(
            Recommendation.issue_id == issue_id
        ).first()
    
    # Generate new recommendation if needed
    if not existing_rec:
        try:
            recommendation = await generate_recommendation(issue, db)
        except Exception as e:
            print(f"❌ Error generating recommendation: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate recommendation: {str(e)}"
            )
    else:
        recommendation = existing_rec
        print(f"ℹ️ Using existing recommendation for issue {issue_id}")
    
    # Determine status
    status = "mock" if recommendation.model_used == "mock-fallback" else "success"
    
    # Return frontend-friendly response
    return RecommendationResponse(
        issue_id=issue.id,
        issue_type=issue.type,
        title=issue.title,
        plain_language_explanation=recommendation.ai_explanation,
        suggested_fix=recommendation.suggested_fix_html,
        before_snippet=recommendation.before_snippet or issue.snippet or "",
        after_snippet=recommendation.after_snippet or recommendation.suggested_fix_html,
        confidence_score=recommendation.confidence_score,
        model_used=recommendation.model_used,
        status=status
    )


@router.delete("/{issue_id}", status_code=204)
async def delete_recommendation(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete recommendation for an issue
    
    Useful for testing or if you want to regenerate a recommendation.
    After deleting, call GET again to generate a fresh recommendation.
    
    **Parameters:**
    - **issue_id**: UUID of the issue whose recommendation to delete
    
    **Example:**
    ```
    DELETE /api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    recommendation = db.query(Recommendation).filter(
        Recommendation.issue_id == issue_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail=f"No recommendation found for issue: {issue_id}"
        )
    
    db.delete(recommendation)
    db.commit()
    
    print(f"🗑️ Deleted recommendation for issue {issue_id}")
    
    return None


# Made with Bob
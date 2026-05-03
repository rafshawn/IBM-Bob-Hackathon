# AI Engineering - Bob Sessions

## Role: AI Engineer (Moe)

### Goal
Transform the platform from detection to intelligent solution - providing AI-powered recommendations that non-technical users can understand and implement.

## Core Responsibilities

### 1. Structured Output
- Force LLM to return valid JSON
- Include explanation + fixed code snippet
- Ensure consistent format
- Validate output structure

### 2. Confidence Scoring
- Return confidence level (0-100%)
- Help users know when to double-check
- Base on multiple factors:
  - Pattern recognition confidence
  - Context completeness
  - Fix complexity

### 3. Automation Simulation
- Create "Auto-fix" preview logic
- Show exact HTML changes
- Highlight differences
- Provide rollback capability

### 4. Context-Aware Recommendations
- Use page context for better suggestions
- Consider surrounding HTML
- Maintain semantic meaning
- Preserve existing styles

## Tech Stack

- **LLM**: IBM WatsonX (preferred) or OpenAI GPT-4
- **Framework**: LangChain (optional, for complex chains)
- **Validation**: Pydantic for output schemas
- **HTML Parsing**: BeautifulSoup4 or lxml
- **Diff Generation**: difflib or similar

## WatsonX Integration

### Setup
```python
from ibm_watson_machine_learning.foundation_models import Model

# Initialize WatsonX
model = Model(
    model_id="meta-llama/llama-2-70b-chat",
    credentials={
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": "YOUR_API_KEY"
    },
    project_id="YOUR_PROJECT_ID"
)
```

### Basic Prompt Pattern
```python
def generate_recommendation(issue: Issue, context: str) -> Recommendation:
    prompt = f"""
You are an accessibility and SEO expert. Analyze this issue and provide a fix.

Issue Type: {issue.type}
Issue Description: {issue.description}
Current HTML:
{context}

Provide your response in this exact JSON format:
{{
    "explanation": "Clear explanation in plain language",
    "suggested_fix_html": "The corrected HTML",
    "confidence_score": 95,
    "reasoning": "Why this fix works"
}}
"""
    
    response = model.generate_text(prompt=prompt)
    return parse_response(response)
```

## Recommendation Engine Architecture

```
Issue + Context
    ↓
Prompt Engineering
    ↓
WatsonX LLM
    ↓
JSON Response
    ↓
Validation (Pydantic)
    ↓
Confidence Scoring
    ↓
Store in Database
    ↓
Return to Frontend
```

## Prompt Engineering Patterns

### 1. Missing Alt Text
```python
MISSING_ALT_TEXT_PROMPT = """
You are helping a public service website improve accessibility.

Issue: An image is missing alt text
Current HTML: {html_snippet}
Page Context: {page_title}

Generate appropriate alt text that:
1. Describes the image content
2. Fits the page context
3. Is concise (< 125 characters)
4. Follows WCAG 2.1 guidelines

Return JSON:
{{
    "explanation": "Why alt text is important for screen readers",
    "suggested_fix_html": "<img src='...' alt='descriptive text'>",
    "confidence_score": 90,
    "reasoning": "Based on image context and page content"
}}
"""
```

### 2. Poor Meta Description
```python
META_DESCRIPTION_PROMPT = """
You are an SEO expert helping improve a public service website.

Issue: Meta description is missing or too short
Current: {current_meta}
Page Title: {page_title}
Page Content Summary: {content_summary}

Generate an effective meta description that:
1. Is 150-160 characters
2. Includes relevant keywords
3. Accurately describes the page
4. Encourages clicks

Return JSON:
{{
    "explanation": "Why meta descriptions matter for SEO",
    "suggested_fix_html": "<meta name='description' content='...'>",
    "confidence_score": 85,
    "reasoning": "Based on page content and SEO best practices"
}}
"""
```

### 3. Heading Hierarchy
```python
HEADING_HIERARCHY_PROMPT = """
You are helping fix heading structure for accessibility.

Issue: {issue_description}
Current Headings:
{heading_structure}

Fix the heading hierarchy to:
1. Have only one H1
2. Follow logical order (H1 → H2 → H3)
3. Not skip levels
4. Maintain semantic meaning

Return JSON:
{{
    "explanation": "Why heading hierarchy matters",
    "suggested_fix_html": "Corrected heading structure",
    "confidence_score": 95,
    "reasoning": "Based on WCAG guidelines"
}}
"""
```

## Output Schema

### Pydantic Model
```python
from pydantic import BaseModel, Field, validator

class AIRecommendation(BaseModel):
    explanation: str = Field(
        ...,
        description="Plain-language explanation for non-technical users",
        min_length=50,
        max_length=500
    )
    suggested_fix_html: str = Field(
        ...,
        description="The corrected HTML code"
    )
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence level (0-100)"
    )
    reasoning: str = Field(
        ...,
        description="Why this fix is recommended"
    )
    
    @validator('confidence_score')
    def validate_confidence(cls, v):
        if v < 50:
            raise ValueError("Confidence too low, manual review needed")
        return v
```

## Confidence Scoring Logic

```python
def calculate_confidence(
    issue_type: str,
    context_completeness: float,
    pattern_match: float,
    fix_complexity: str
) -> int:
    """
    Calculate confidence score based on multiple factors
    
    Args:
        issue_type: Type of issue (seo, accessibility, etc.)
        context_completeness: How much context we have (0-1)
        pattern_match: How well it matches known patterns (0-1)
        fix_complexity: 'simple', 'medium', 'complex'
    
    Returns:
        Confidence score (0-100)
    """
    base_confidence = {
        'seo': 85,
        'accessibility': 90,
        'qa': 75
    }.get(issue_type, 70)
    
    # Adjust for context
    context_adjustment = context_completeness * 10
    
    # Adjust for pattern match
    pattern_adjustment = pattern_match * 10
    
    # Adjust for complexity
    complexity_penalty = {
        'simple': 0,
        'medium': -5,
        'complex': -15
    }.get(fix_complexity, -10)
    
    final_score = base_confidence + context_adjustment + pattern_adjustment + complexity_penalty
    
    return max(0, min(100, int(final_score)))
```

## Auto-Fix Preview

### Generate Diff
```python
import difflib
from typing import Tuple

def generate_diff(original: str, fixed: str) -> Tuple[str, str]:
    """
    Generate before/after diff for display
    
    Returns:
        (html_diff, text_diff)
    """
    # Text diff
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        fixed.splitlines(keepends=True),
        fromfile='before',
        tofile='after'
    )
    text_diff = ''.join(diff)
    
    # HTML diff for display
    html_diff = difflib.HtmlDiff().make_table(
        original.splitlines(),
        fixed.splitlines(),
        fromdesc='Before',
        todesc='After'
    )
    
    return html_diff, text_diff
```

### Preview Structure
```python
class FixPreview(BaseModel):
    before_html: str
    after_html: str
    diff_html: str
    changes_summary: List[str]
    estimated_impact: str  # "High", "Medium", "Low"
```

## API Endpoints

### Get Recommendation
```python
@router.get("/recommendations/{issue_id}")
async def get_recommendation(
    issue_id: str,
    db: Session = Depends(get_db)
):
    # Get issue from database
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Check if recommendation already exists
    existing = db.query(Recommendation).filter(
        Recommendation.issue_id == issue_id
    ).first()
    
    if existing:
        return existing
    
    # Generate new recommendation
    recommendation = await generate_recommendation(issue)
    
    # Store in database
    db.add(recommendation)
    db.commit()
    
    return recommendation
```

### Batch Recommendations
```python
@router.post("/recommendations/batch")
async def generate_batch_recommendations(
    issue_ids: List[str],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Generate recommendations in background
    background_tasks.add_task(
        process_batch_recommendations,
        issue_ids,
        db
    )
    
    return {"status": "processing", "count": len(issue_ids)}
```

## Error Handling

### LLM Failures
```python
async def generate_recommendation_with_fallback(issue: Issue) -> Recommendation:
    try:
        # Try AI generation
        return await generate_ai_recommendation(issue)
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        # Fallback to rule-based
        return generate_rule_based_recommendation(issue)
```

### Invalid Output
```python
def validate_and_fix_output(raw_output: str) -> dict:
    try:
        # Try to parse JSON
        data = json.loads(raw_output)
        
        # Validate with Pydantic
        AIRecommendation(**data)
        
        return data
    except json.JSONDecodeError:
        # Try to extract JSON from text
        return extract_json_from_text(raw_output)
    except ValidationError as e:
        # Log validation errors
        logger.error(f"Validation failed: {e}")
        raise
```

## Testing Strategy

### Unit Tests
```python
def test_recommendation_generation():
    issue = Issue(
        type="accessibility",
        description="Missing alt text",
        snippet="<img src='test.jpg'>"
    )
    
    recommendation = generate_recommendation(issue)
    
    assert recommendation.confidence_score >= 50
    assert "alt=" in recommendation.suggested_fix_html
    assert len(recommendation.explanation) > 50
```

### Integration Tests
```python
async def test_watsonx_integration():
    # Test with real WatsonX API
    response = await call_watsonx(test_prompt)
    assert response is not None
    assert "explanation" in response
```

### Quality Tests
```python
def test_recommendation_quality():
    # Test that recommendations are helpful
    recommendation = generate_recommendation(test_issue)
    
    # Check readability
    assert is_readable(recommendation.explanation)
    
    # Check HTML validity
    assert is_valid_html(recommendation.suggested_fix_html)
    
    # Check confidence is reasonable
    assert 50 <= recommendation.confidence_score <= 100
```

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_recommendation(issue_hash: str) -> Recommendation:
    # Cache recommendations for similar issues
    pass
```

### Batch Processing
```python
async def process_batch(issues: List[Issue]) -> List[Recommendation]:
    # Process multiple issues in parallel
    tasks = [generate_recommendation(issue) for issue in issues]
    return await asyncio.gather(*tasks)
```

## Integration Points

### With Backend
- Receive issue context and HTML snippets
- Store recommendations in database
- Provide API endpoints for frontend
- Handle errors gracefully

### With Frontend
- Return structured JSON
- Include confidence scores
- Provide before/after previews
- Support real-time updates

## Session Documentation

Document your AI engineering sessions:
- `session_001_watsonx_setup.md` - WatsonX integration
- `session_002_prompt_engineering.md` - Prompt development
- `session_003_confidence_scoring.md` - Scoring algorithm
- `session_004_testing_quality.md` - Quality assurance
- etc.

## Resources

- [IBM WatsonX Documentation](https://www.ibm.com/docs/en/watsonx)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [SEO Best Practices](https://developers.google.com/search/docs)
- [LangChain Documentation](https://python.langchain.com/)

## Success Criteria

- [ ] AI provides valid HTML fixes for 3+ WCAG failures
- [ ] Recommendations are understandable to non-technical users
- [ ] Confidence scores are accurate
- [ ] Response time < 5 seconds per recommendation
- [ ] Fallback system works when AI fails
- [ ] Output is consistently structured
- [ ] Integration with backend is seamless

---

**Remember**: Your AI recommendations are the "magic" that differentiates this platform. Make them accurate, understandable, and actionable!
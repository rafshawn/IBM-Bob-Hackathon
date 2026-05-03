# PublicPulse AI - Integration Readiness Report

**Version:** 1.0  
**Date:** May 3, 2026  
**Product Lead:** Frank Melgoza  
**Status:** 🟡 In Progress - Critical Gaps Identified

---

## Executive Summary

PublicPulse AI has a solid foundation with backend API structure, database models, and clear documentation. However, **critical integration gaps exist** that must be addressed for the MVP demo, particularly around the "Bob makes the fix" action loop and AI recommendation generation.

### Current State: 🟡 60% Ready
- ✅ **Backend API Structure**: Complete
- ✅ **Database Schema**: Complete
- ✅ **Documentation**: Excellent
- 🟡 **Crawler Implementation**: Placeholder only
- 🟡 **Issue Detection**: Not implemented
- ❌ **AI Integration**: Missing
- ❌ **Frontend**: Not started
- ❌ **Bob Action Loop**: Not defined

---

## Architecture Overview

### Intended System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Astro + Vue)                        │
│  User enters URL → Triggers scan → Polls for progress           │
│  Views results → Selects issue → Requests AI fix                │
│  Reviews fix → Sees Bob session evidence                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓ REST API
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  Receives scan request → Queues background task                 │
│  Crawls with Playwright → Detects issues → Stores in DB        │
│  Serves results → Triggers AI recommendations                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                             │
│  Sites → Pages → Issues → Recommendations                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    AI ENGINE (WatsonX)                           │
│  Receives issue context → Generates structured fix              │
│  Returns JSON: {fix_html, explanation, confidence}              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    IBM BOB ACTION LOOP                           │
│  Bob generates fix code → Stores in recommendations             │
│  Session evidence captured → Displayed in UI                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Contracts

### 1. Scan Initiation

**Endpoint:** `POST /api/v1/scans`

**Frontend Request:**
```typescript
interface ScanRequest {
  url: string;           // Valid HTTP/HTTPS URL
  max_pages?: number;    // Default: 50, Max: 100
  max_depth?: number;    // Default: 3, Max: 5
}
```

**Backend Response:**
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2026-05-03T04:00:00Z"
}
```

**Status:** ✅ Implemented

---

### 2. Scan Status Polling

**Endpoint:** `GET /api/v1/scans/{scan_id}`

**Frontend Polling Logic:**
```typescript
// Poll every 2 seconds until completed/failed
async function pollScanStatus(scanId: string) {
  const interval = setInterval(async () => {
    const response = await fetch(`/api/v1/scans/${scanId}`);
    const data = await response.json();
    
    if (data.status === 'completed' || data.status === 'failed') {
      clearInterval(interval);
      // Navigate to results or show error
    }
    
    // Update progress UI
    updateProgress(data.progress, data.pages_scanned);
  }, 2000);
}
```

**Backend Response:**
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": 45,
  "pages_scanned": 12,
  "total_pages": 27,
  "created_at": "2026-05-03T04:00:00Z",
  "updated_at": "2026-05-03T04:01:30Z",
  "error_message": null
}
```

**Status:** ✅ Implemented (but crawler is placeholder)

---

### 3. Scan Results

**Endpoint:** `GET /api/v1/scans/{scan_id}/results`

**Backend Response:**
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "domain_url": "https://example.gov",
  "status": "completed",
  "global_score": 75.5,
  "created_at": "2026-05-03T04:00:00Z",
  "pages_scanned": 25,
  "total_issues": 42,
  "issues_by_type": {
    "seo": 15,
    "accessibility": 20,
    "qa": 7
  },
  "issues_by_severity": {
    "high": 8,
    "medium": 18,
    "low": 16
  },
  "top_issues": [
    {
      "id": "issue-uuid-1",
      "type": "accessibility",
      "severity": "high",
      "title": "Missing alt text on images",
      "description": "5 images are missing alternative text",
      "priority_score": 95,
      "page_url": "https://example.gov/",
      "snippet": "<img src='/hero.jpg' class='hero-image'>",
      "element_selector": "img.hero-image",
      "wcag_criterion": "1.1.1",
      "detected_at": "2026-05-03T04:01:00Z"
    }
  ],
  "pages": [
    {
      "id": "page-uuid-1",
      "url": "https://example.gov/",
      "title": "Home - Example Government",
      "meta_description": "Official government website",
      "status_code": 200,
      "crawled_at": "2026-05-03T04:00:30Z"
    }
  ]
}
```

**Status:** ✅ Implemented (but returns empty data without crawler)

---

### 4. Issue List with Filters

**Endpoint:** `GET /api/v1/issues`

**Query Parameters:**
```typescript
interface IssueFilters {
  scan_id?: string;
  page_id?: string;
  type?: 'seo' | 'accessibility' | 'qa';
  severity?: 'high' | 'medium' | 'low';
  page?: number;        // Default: 1
  page_size?: number;   // Default: 50, Max: 100
}
```

**Backend Response:**
```json
{
  "issues": [
    {
      "id": "issue-uuid-1",
      "page_id": "page-uuid-1",
      "type": "accessibility",
      "severity": "high",
      "title": "Missing alt text on image",
      "description": "Image at /hero.jpg is missing alternative text",
      "priority_score": 95,
      "snippet": "<img src='/hero.jpg'>",
      "element_selector": "img.hero-image",
      "wcag_criterion": "1.1.1",
      "detected_at": "2026-05-03T04:01:00Z",
      "page_url": "https://example.gov/"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 50
}
```

**Status:** ✅ Implemented

---

### 5. AI Recommendation (CRITICAL - NOT IMPLEMENTED)

**Endpoint:** `GET /api/v1/recommendations/{issue_id}` ❌ **MISSING**

**Expected Backend Response:**
```json
{
  "id": "rec-uuid-1",
  "issue_id": "issue-uuid-1",
  "suggested_fix_html": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "ai_explanation": "Added descriptive alt text that explains what the image shows. This helps screen reader users understand the visual content and meets WCAG 2.1 Success Criterion 1.1.1 (Non-text Content).",
  "confidence_score": 95.0,
  "reasoning": "Based on the image context and page content, this alt text accurately describes the visual information while being concise and meaningful.",
  "before_snippet": "<img src='/hero.jpg' class='hero-image'>",
  "after_snippet": "<img src='/hero.jpg' alt='Government building exterior with American flag' class='hero-image'>",
  "diff_html": "<div class='diff'>...</div>",
  "created_at": "2026-05-03T04:02:00Z",
  "model_used": "watsonx-llama-2-70b",
  "bob_session_id": "bob-session-uuid-1"
}
```

**Frontend Usage:**
```typescript
async function getRecommendation(issueId: string) {
  const response = await fetch(`/api/v1/recommendations/${issueId}`);
  const recommendation = await response.json();
  
  // Display in UI:
  // - Before/after code comparison
  // - Plain-language explanation
  // - Confidence score badge
  // - Bob session evidence link
  
  return recommendation;
}
```

**Status:** ❌ **NOT IMPLEMENTED - CRITICAL FOR MVP**

---

### 6. Bob Session Evidence (NEW - REQUIRED FOR DEMO)

**Endpoint:** `GET /api/v1/recommendations/{rec_id}/bob-session` ❌ **MISSING**

**Expected Response:**
```json
{
  "recommendation_id": "rec-uuid-1",
  "bob_session_id": "bob-session-uuid-1",
  "session_date": "2026-05-03T04:02:00Z",
  "task_description": "Generate accessible alt text for hero image",
  "bob_interactions": [
    {
      "timestamp": "2026-05-03T04:02:05Z",
      "user_prompt": "Generate alt text for this image: <img src='/hero.jpg'>",
      "bob_response": "I'll create descriptive alt text that meets WCAG guidelines...",
      "code_generated": "<img src='/hero.jpg' alt='Government building exterior with American flag'>"
    }
  ],
  "session_summary": "Bob analyzed the image context and generated WCAG-compliant alt text",
  "evidence_url": "/bob-sessions/ai-engineering/session_hero_alt_text.md"
}
```

**Status:** ❌ **NOT IMPLEMENTED - REQUIRED FOR DEMO**

---

## IBM Bob Action Loop Integration

### The "Bob Makes the Fix" Flow

This is the **key differentiator** for the demo. Here's how it should work:

```
1. User selects high-priority issue
   ↓
2. Frontend calls: GET /api/v1/recommendations/{issue_id}
   ↓
3. Backend checks if recommendation exists
   ↓
4. If NOT exists:
   a. Backend calls AI service (WatsonX)
   b. AI generates structured fix
   c. Backend stores recommendation
   d. Backend creates Bob session record
   ↓
5. Backend returns recommendation with Bob session ID
   ↓
6. Frontend displays:
   - Before/after code comparison
   - Plain-language explanation
   - Confidence score
   - "View Bob Session" button
   ↓
7. User clicks "View Bob Session"
   ↓
8. Frontend calls: GET /api/v1/recommendations/{rec_id}/bob-session
   ↓
9. Frontend displays Bob session evidence:
   - Task description
   - Bob's analysis
   - Code generated
   - Link to full session markdown
```

### Implementation Requirements

#### Backend (Shawn + Moe)

**File:** `src/backend/app/routers/recommendations.py` ❌ **MISSING**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Issue, Recommendation
from app.services.ai_service import generate_ai_recommendation
from app.services.bob_session import create_bob_session_record

router = APIRouter()

@router.get("/recommendations/{issue_id}")
async def get_recommendation(
    issue_id: str,
    force_regenerate: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get or generate AI recommendation for an issue
    """
    # Get issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Check for existing recommendation
    if not force_regenerate:
        existing = db.query(Recommendation).filter(
            Recommendation.issue_id == issue_id
        ).first()
        if existing:
            return existing
    
    # Generate new recommendation using AI
    recommendation = await generate_ai_recommendation(issue, db)
    
    # Create Bob session record
    bob_session = await create_bob_session_record(
        recommendation_id=recommendation.id,
        issue=issue,
        fix_generated=recommendation.suggested_fix_html
    )
    
    return recommendation

@router.get("/recommendations/{rec_id}/bob-session")
async def get_bob_session(
    rec_id: str,
    db: Session = Depends(get_db)
):
    """
    Get Bob session evidence for a recommendation
    """
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == rec_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Retrieve Bob session data
    bob_session = get_bob_session_data(recommendation.id)
    
    return bob_session
```

**File:** `src/backend/app/services/ai_service.py` ❌ **MISSING**

```python
from app.models import Issue, Recommendation
from app.config import settings
import uuid
from datetime import datetime

async def generate_ai_recommendation(issue: Issue, db) -> Recommendation:
    """
    Generate AI-powered recommendation using WatsonX
    """
    # Build context from issue
    context = {
        "issue_type": issue.type,
        "description": issue.description,
        "html_snippet": issue.snippet,
        "page_url": issue.page.url,
        "wcag_criterion": issue.wcag_criterion
    }
    
    # Call WatsonX API (or mock for MVP)
    ai_response = await call_watsonx_api(context)
    
    # Create recommendation record
    recommendation = Recommendation(
        id=str(uuid.uuid4()),
        issue_id=issue.id,
        suggested_fix_html=ai_response["suggested_fix_html"],
        ai_explanation=ai_response["explanation"],
        confidence_score=ai_response["confidence_score"],
        reasoning=ai_response["reasoning"],
        before_snippet=issue.snippet,
        after_snippet=ai_response["suggested_fix_html"],
        created_at=datetime.utcnow(),
        model_used="watsonx-llama-2-70b"
    )
    
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    return recommendation

async def call_watsonx_api(context: dict) -> dict:
    """
    Call WatsonX API or return mock data for MVP
    """
    # TODO: Implement actual WatsonX integration
    # For MVP, return structured mock data
    
    if context["issue_type"] == "accessibility" and "alt" in context["description"].lower():
        return {
            "suggested_fix_html": context["html_snippet"].replace(">", " alt='Descriptive alt text'>"),
            "explanation": "Added descriptive alt text to meet WCAG 2.1 Success Criterion 1.1.1",
            "confidence_score": 95.0,
            "reasoning": "Based on image context and accessibility guidelines"
        }
    
    # Add more mock responses for other issue types
    return {
        "suggested_fix_html": "<!-- Fixed HTML -->",
        "explanation": "AI-generated fix explanation",
        "confidence_score": 85.0,
        "reasoning": "Based on best practices"
    }
```

#### Frontend (Arvin)

**Component:** `src/frontend/src/components/RecommendationView.vue` ❌ **MISSING**

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';

const props = defineProps<{ issueId: string }>();

const recommendation = ref(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    const response = await fetch(`/api/v1/recommendations/${props.issueId}`);
    recommendation.value = await response.json();
  } catch (e) {
    error.value = 'Failed to load recommendation';
  } finally {
    loading.value = false;
  }
});

async function viewBobSession() {
  const response = await fetch(`/api/v1/recommendations/${recommendation.value.id}/bob-session`);
  const session = await response.json();
  // Display session in modal or new page
}
</script>

<template>
  <div class="recommendation-view">
    <div v-if="loading">Loading AI recommendation...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="recommendation">
      <!-- Confidence Score -->
      <div class="confidence-badge">
        {{ recommendation.confidence_score }}% Confidence
      </div>
      
      <!-- Explanation -->
      <div class="explanation">
        <h3>What's Wrong</h3>
        <p>{{ recommendation.ai_explanation }}</p>
      </div>
      
      <!-- Before/After Code -->
      <div class="code-comparison">
        <div class="before">
          <h4>Before</h4>
          <pre><code>{{ recommendation.before_snippet }}</code></pre>
        </div>
        <div class="after">
          <h4>After (Suggested Fix)</h4>
          <pre><code>{{ recommendation.after_snippet }}</code></pre>
        </div>
      </div>
      
      <!-- Bob Session Evidence -->
      <button @click="viewBobSession" class="bob-session-btn">
        🤖 View IBM Bob Session
      </button>
    </div>
  </div>
</template>
```

---

## What Must Work for MVP

### Critical Path (Must Have)

1. ✅ **Backend API responds** to scan requests
2. ❌ **Crawler actually crawls** pages (currently placeholder)
3. ❌ **Issue detection** identifies real problems
4. ❌ **AI recommendations** generate valid fixes
5. ❌ **Bob session tracking** captures evidence
6. ❌ **Frontend displays** scan results
7. ❌ **Frontend shows** AI recommendations
8. ❌ **Frontend links** to Bob session evidence

### Minimum Viable Features

- **Scan 1 website** (10-25 pages)
- **Detect 3 issue types**: Missing alt text, missing meta description, heading hierarchy
- **Generate 3 AI fixes**: One for each issue type
- **Show Bob evidence**: Link to markdown session files
- **Display results**: Simple table with filters

---

## What Can Be Mocked

### For Time Constraints

1. **WatsonX API**: Use rule-based mock responses
   ```python
   # Mock AI responses for common issues
   MOCK_RECOMMENDATIONS = {
       "missing_alt_text": {
           "fix": "<img src='...' alt='Descriptive text'>",
           "explanation": "Added alt text for accessibility",
           "confidence": 95
       },
       "missing_meta": {
           "fix": "<meta name='description' content='...'>",
           "explanation": "Added meta description for SEO",
           "confidence": 90
       }
   }
   ```

2. **Bob Session Data**: Pre-created markdown files
   ```markdown
   # Bob Session: Alt Text Generation
   
   **Task**: Generate alt text for hero image
   **Date**: 2026-05-03
   
   ## User Request
   "Generate alt text for <img src='/hero.jpg'>"
   
   ## Bob's Analysis
   Based on the image context and WCAG guidelines...
   
   ## Generated Fix
   `<img src='/hero.jpg' alt='Government building exterior'>`
   ```

3. **Actual Crawling**: Use pre-seeded demo data
   ```python
   # Demo data for example.gov
   DEMO_SCAN_DATA = {
       "pages": [...],
       "issues": [...]
   }
   ```

---

## What Should Be Cut If Time Is Short

### Nice-to-Have Features (Cut First)

1. ❌ Historical tracking
2. ❌ Scheduled scans
3. ❌ Email notifications
4. ❌ Export to PDF
5. ❌ Advanced analytics
6. ❌ User authentication
7. ❌ Team collaboration
8. ❌ Custom scoring algorithms

### Simplifications

- **Limit to 1 scan at a time** (no concurrent scans)
- **Max 25 pages** instead of 50
- **3 issue types only** (alt text, meta, headings)
- **No pagination** (show all results on one page)
- **Static Bob sessions** (pre-written, not generated)

---

## Role-Specific Blockers & Questions

### Frontend (Arvin)

**Blockers:**
- ❌ No frontend codebase exists yet
- ❌ API endpoints not fully tested
- ❌ No design system chosen

**Questions:**
1. Should we use TailwindCSS or getdesign.md?
2. What's the exact API base URL for development?
3. Do we need authentication for the MVP?
4. Should we support mobile or desktop-only for demo?

**Action Items:**
- [ ] Initialize Astro project
- [ ] Create basic dashboard layout
- [ ] Implement ScanForm component
- [ ] Build IssueTable component
- [ ] Create RecommendationView component
- [ ] Test API integration

---

### Backend (Shawn)

**Blockers:**
- ❌ Playwright crawler is placeholder only
- ❌ No issue detection logic implemented
- ❌ No recommendation endpoints

**Questions:**
1. Should we use real Playwright or mock data for demo?
2. What's the priority order for issue detection?
3. How should we handle crawler errors?
4. Should we implement rate limiting?

**Action Items:**
- [ ] Implement Playwright crawler
- [ ] Build issue detection analyzers
- [ ] Create recommendation endpoints
- [ ] Add Bob session tracking
- [ ] Test with real websites
- [ ] Seed demo database

---

### AI Engineering (Moe)

**Blockers:**
- ❌ No WatsonX integration code
- ❌ No prompt engineering done
- ❌ No confidence scoring logic

**Questions:**
1. Do we have WatsonX API credentials?
2. Should we use LangChain or direct API calls?
3. What's the fallback if WatsonX fails?
4. How do we validate AI output quality?

**Action Items:**
- [ ] Set up WatsonX credentials
- [ ] Design prompt templates
- [ ] Implement AI service layer
- [ ] Create mock responses for demo
- [ ] Build confidence scoring
- [ ] Test recommendation quality

---

### Product/Integration (Frank)

**Blockers:**
- ❌ No end-to-end integration yet
- ❌ Bob action loop not defined
- ❌ Demo flow not tested

**Questions:**
1. What's the exact demo scenario?
2. Which website should we scan for demo?
3. How do we show Bob session evidence?
4. What's the backup plan if live demo fails?

**Action Items:**
- [ ] Define exact demo flow
- [ ] Create integration test plan
- [ ] Coordinate team sync meetings
- [ ] Prepare demo script
- [ ] Test end-to-end flow
- [ ] Create backup demo video

---

## Integration Testing Plan

### Phase 1: Component Testing (Days 1-2)
- Backend API endpoints work independently
- Frontend components render correctly
- AI service returns valid responses

### Phase 2: Integration Testing (Days 3-4)
- Frontend → Backend communication
- Backend → AI service communication
- Database persistence works
- Bob session tracking functions

### Phase 3: End-to-End Testing (Day 5)
- Complete user flow works
- Demo scenario runs smoothly
- Error handling is graceful
- Performance is acceptable

### Phase 4: Demo Rehearsal (Day 6)
- Full demo walkthrough 3x
- Backup plans tested
- Team roles assigned
- Timing perfected

---

## Recommended Next Steps

### Immediate (Next 24 Hours)

1. **Backend Team**:
   - Implement basic Playwright crawler
   - Create 3 issue detection rules
   - Add recommendation endpoints

2. **AI Team**:
   - Set up mock AI responses
   - Create Bob session templates
   - Design recommendation format

3. **Frontend Team**:
   - Initialize Astro project
   - Create basic dashboard
   - Implement scan form

4. **Product Team**:
   - Define exact demo scenario
   - Create integration checklist
   - Schedule daily standups

### Short Term (Next 3 Days)

1. **Integration**:
   - Connect frontend to backend
   - Test scan flow end-to-end
   - Implement Bob session display

2. **Testing**:
   - Seed demo database
   - Test with real website
   - Fix critical bugs

3. **Demo Prep**:
   - Write demo script
   - Practice delivery
   - Create backup video

---

## Success Criteria

### Technical
- [ ] Can scan a website and detect issues
- [ ] AI generates valid recommendations
- [ ] Bob session evidence is visible
- [ ] Frontend displays all data correctly
- [ ] No critical errors during demo

### User Experience
- [ ] Non-technical user can complete flow
- [ ] Results are understandable
- [ ] Recommendations are actionable
- [ ] Bob's role is clear

### Demo Impact
- [ ] Shows clear value proposition
- [ ] Demonstrates AI intelligence
- [ ] Highlights Bob's contribution
- [ ] Impresses judges

---

## Conclusion

PublicPulse AI has excellent documentation and a solid foundation, but **critical implementation gaps exist**. The team must focus on:

1. **Implementing the crawler and issue detection**
2. **Building the AI recommendation system**
3. **Creating the Bob action loop integration**
4. **Developing the frontend dashboard**

With focused effort and clear priorities, the MVP can be delivered for a successful demo. The key is to **start with the critical path** and **mock what's not essential**.

---

**Next Document:** [FINAL_DEMO_READINESS.md](FINAL_DEMO_READINESS.md)
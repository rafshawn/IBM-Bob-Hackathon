# Recommendation API - Frontend Integration Guide

**Version:** 1.0  
**Date:** May 3, 2026  
**Status:** ✅ Ready for Integration

---

## Overview

The Recommendation API provides AI-powered fix suggestions for detected issues. When a user clicks on an issue, the frontend can request a recommendation that includes:

- Plain-language explanation (non-technical)
- Suggested HTML fix
- Before/after code snippets
- Confidence score
- Status (real AI or mock fallback)

---

## Endpoint

### GET /api/v1/recommendations/{issue_id}

Get or generate an AI recommendation for a specific issue.

**Base URL:** `http://localhost:8000/api/v1`

**Full URL:** `http://localhost:8000/api/v1/recommendations/{issue_id}`

---

## Request

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_id` | string (UUID) | Yes | The ID of the issue to get recommendation for |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `force_regenerate` | boolean | No | false | If true, generates a new recommendation even if one exists |

### Example Request

```bash
# Get recommendation for an issue
curl http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000

# Force regenerate recommendation
curl "http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000?force_regenerate=true"
```

---

## Response

### Success Response (200 OK)

```json
{
  "issue_id": "550e8400-e29b-41d4-a716-446655440000",
  "issue_type": "accessibility",
  "title": "Missing alt text on image",
  "plain_language_explanation": "Images need alternative text (alt text) so screen readers can describe them to visually impaired users. This is required by WCAG 2.1 and helps everyone understand your content.",
  "suggested_fix": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "before_snippet": "<img src='/hero.jpg'>",
  "after_snippet": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "confidence_score": 95.0,
  "model_used": "mock-fallback",
  "status": "mock"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `issue_id` | string | UUID of the issue |
| `issue_type` | string | Type of issue: "accessibility", "seo", or "qa" |
| `title` | string | Issue title |
| `plain_language_explanation` | string | Non-technical explanation of the issue and fix |
| `suggested_fix` | string | The corrected HTML code |
| `before_snippet` | string | Original HTML with the issue |
| `after_snippet` | string | Fixed HTML |
| `confidence_score` | number | AI confidence (0-100) |
| `model_used` | string | AI model used (e.g., "watsonx-llama-2-70b" or "mock-fallback") |
| `status` | string | "success" (real AI), "mock" (fallback), or "error" |

### Error Responses

**404 Not Found** - Issue doesn't exist
```json
{
  "detail": "Issue not found with ID: 550e8400-e29b-41d4-a716-446655440000"
}
```

**500 Internal Server Error** - Failed to generate recommendation
```json
{
  "detail": "Failed to generate recommendation: [error details]"
}
```

---

## Frontend Integration

### TypeScript Interface

```typescript
interface RecommendationResponse {
  issue_id: string;
  issue_type: 'accessibility' | 'seo' | 'qa';
  title: string;
  plain_language_explanation: string;
  suggested_fix: string;
  before_snippet: string;
  after_snippet: string;
  confidence_score: number;
  model_used: string;
  status: 'success' | 'mock' | 'error';
}
```

### API Client Function

```typescript
// src/lib/api.ts
const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function getRecommendation(
  issueId: string,
  forceRegenerate: boolean = false
): Promise<RecommendationResponse> {
  const url = `${API_BASE}/recommendations/${issueId}${
    forceRegenerate ? '?force_regenerate=true' : ''
  }`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to get recommendation: ${response.statusText}`);
  }
  
  return response.json();
}
```

### Vue Component Example

```vue
<!-- components/RecommendationView.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getRecommendation } from '../lib/api';
import type { RecommendationResponse } from '../lib/types';

const props = defineProps<{ issueId: string }>();

const recommendation = ref<RecommendationResponse | null>(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    recommendation.value = await getRecommendation(props.issueId);
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load recommendation';
  } finally {
    loading.value = false;
  }
});

function getConfidenceBadgeClass(score: number): string {
  if (score >= 90) return 'badge-high';
  if (score >= 75) return 'badge-medium';
  return 'badge-low';
}

function getStatusBadgeClass(status: string): string {
  if (status === 'success') return 'badge-success';
  if (status === 'mock') return 'badge-warning';
  return 'badge-error';
}
</script>

<template>
  <div class="recommendation-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Generating AI recommendation...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="$emit('retry')">Try Again</button>
    </div>
    
    <!-- Success State -->
    <div v-else-if="recommendation" class="recommendation">
      <!-- Header with Badges -->
      <div class="header">
        <h3>AI Recommendation</h3>
        <div class="badges">
          <span :class="['badge', getConfidenceBadgeClass(recommendation.confidence_score)]">
            {{ recommendation.confidence_score }}% Confidence
          </span>
          <span :class="['badge', getStatusBadgeClass(recommendation.status)]">
            {{ recommendation.status === 'mock' ? 'Demo Mode' : 'AI Powered' }}
          </span>
        </div>
      </div>
      
      <!-- Explanation -->
      <div class="explanation">
        <h4>What's Wrong & How to Fix It</h4>
        <p>{{ recommendation.plain_language_explanation }}</p>
      </div>
      
      <!-- Code Comparison -->
      <div class="code-comparison">
        <div class="before">
          <h4>❌ Before (Current Code)</h4>
          <pre><code>{{ recommendation.before_snippet }}</code></pre>
        </div>
        
        <div class="arrow">→</div>
        Now let me create comprehensive documentation for the frontend team on how to use the new recommendation endpoint.

<write_to_file>
<path>docs/RECOMMENDATION_API.md</path>
<content>
# Recommendation API - Frontend Integration Guide

**Version:** 1.0  
**Date:** May 3, 2026  
**Status:** ✅ Ready for Integration

---

## Overview

The Recommendation API provides AI-powered fix suggestions for detected issues. When a user clicks on an issue, the frontend can request a recommendation that includes:

- Plain-language explanation (non-technical)
- Suggested HTML fix
- Before/after code snippets
- Confidence score
- Status (real AI or mock fallback)

---

## Endpoint

### GET /api/v1/recommendations/{issue_id}

Get or generate an AI recommendation for a specific issue.

**Base URL:** `http://localhost:8000/api/v1`

**Full URL:** `http://localhost:8000/api/v1/recommendations/{issue_id}`

---

## Request

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_id` | string (UUID) | Yes | The ID of the issue to get recommendation for |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `force_regenerate` | boolean | No | false | If true, generates a new recommendation even if one exists |

### Example Request

```bash
# Get recommendation for an issue
curl http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000

# Force regenerate recommendation
curl "http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000?force_regenerate=true"
```

---

## Response

### Success Response (200 OK)

```json
{
  "issue_id": "550e8400-e29b-41d4-a716-446655440000",
  "issue_type": "accessibility",
  "title": "Missing alt text on image",
  "plain_language_explanation": "Images need alternative text (alt text) so screen readers can describe them to visually impaired users. This is required by WCAG 2.1 and helps everyone understand your content.",
  "suggested_fix": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "before_snippet": "<img src='/hero.jpg'>",
  "after_snippet": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "confidence_score": 95.0,
  "model_used": "mock-fallback",
  "status": "mock"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `issue_id` | string | UUID of the issue |
| `issue_type` | string | Type of issue: "accessibility", "seo", or "qa" |
| `title` | string | Issue title |
| `plain_language_explanation` | string | Non-technical explanation of the issue and fix |
| `suggested_fix` | string | The corrected HTML code |
| `before_snippet` | string | Original HTML with the issue |
| `after_snippet` | string | Fixed HTML |
| `confidence_score` | number | AI confidence (0-100) |
| `model_used` | string | AI model used (e.g., "watsonx-llama-2-70b" or "mock-fallback") |
| `status` | string | "success" (real AI), "mock" (fallback), or "error" |

### Error Responses

**404 Not Found** - Issue doesn't exist
```json
{
  "detail": "Issue not found with ID: 550e8400-e29b-41d4-a716-446655440000"
}
```

**500 Internal Server Error** - Failed to generate recommendation
```json
{
  "detail": "Failed to generate recommendation: [error details]"
}
```

---

## Frontend Integration

### TypeScript Interface

```typescript
interface RecommendationResponse {
  issue_id: string;
  issue_type: 'accessibility' | 'seo' | 'qa';
  title: string;
  plain_language_explanation: string;
  suggested_fix: string;
  before_snippet: string;
  after_snippet: string;
  confidence_score: number;
  model_used: string;
  status: 'success' | 'mock' | 'error';
}
```

### API Client Function

```typescript
// src/lib/api.ts
const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function getRecommendation(
  issueId: string,
  forceRegenerate: boolean = false
): Promise<RecommendationResponse> {
  const url = `${API_BASE}/recommendations/${issueId}${
    forceRegenerate ? '?force_regenerate=true' : ''
  }`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to get recommendation: ${response.statusText}`);
  }
  
  return response.json();
}
```

### Vue Component Example

```vue
<!-- components/RecommendationView.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getRecommendation } from '../lib/api';
import type { RecommendationResponse } from '../lib/types';

const props = defineProps<{ issueId: string }>();

const recommendation = ref<RecommendationResponse | null>(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    recommendation.value = await getRecommendation(props.issueId);
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load recommendation';
  } finally {
    loading.value = false;
  }
});

function getConfidenceBadgeClass(score: number): string {
  if (score >= 90) return 'badge-high';
  if (score >= 75) return 'badge-medium';
  return 'badge-low';
}

function getStatusBadgeClass(status: string): string {
  if (status === 'success') return 'badge-success';
  if (status === 'mock') return 'badge-warning';
  return 'badge-error';
}
</script>

<template>
  <div class="recommendation-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Generating AI recommendation...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="$emit('retry')">Try Again</button>
    </div>
    
    <!-- Success State -->
    <div v-else-if="recommendation" class="recommendation">
      <!-- Header with Badges -->
      <div class="header">
        <h3>AI Recommendation</h3>
        <div class="badges">
          <span :class="['badge', getConfidenceBadgeClass(recommendation.confidence_score)]">
            {{ recommendation.confidence_score }}% Confidence
          </span>
          <span :class="['badge', getStatusBadgeClass(recommendation.status)]">
            {{ recommendation.status === 'mock' ? 'Demo Mode' : 'AI Powered' }}
          </span>
        </div>
      </div>
      
      <!-- Explanation -->
      <div class="explanation">
        <h4>What's Wrong & How to Fix It</h4>
        <p>{{ recommendation.plain_language_explanation }}</p>
      </div>
      
      <!-- Code Comparison -->
      <div class="code-comparison">
        <div class="before">
          <h4>❌ Before (Current Code)</h4>
          <pre><code>{{ recommendation.before_snippet }}</code></pre>
        </div>
        
        <div class="arrow">→</div>
        
        <div class="after">
          <h4>✅ After (Suggested Fix)</h4>
          <pre><code>{{ recommendation.after_snippet }}</code></pre>
        </div>
      </div>
      
      <!-- Copy Button -->
      <div class="actions">
        <button @click="copyToClipboard(recommendation.after_snippet)">
          Copy Fix to Clipboard
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recommendation-view {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
  background: white;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.badges {
  display: flex;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge-high {
  background: #10b981;
  color: white;
}

.badge-medium {
  background: #f59e0b;
  color: white;
}

.badge-low {
  background: #ef4444;
  color: white;
}

.badge-success {
  background: #10b981;
  color: white;
}

.badge-warning {
  background: #f59e0b;
  color: white;
}

.badge-error {
  background: #ef4444;
  color: white;
}

.explanation {
  margin: 1.5rem 0;
  line-height: 1.6;
}

.code-comparison {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
  font-family: monospace;
  font-size: 0.875rem;
}

.code-comparison > div {
  flex: 1;
}

.code-comparison pre {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 4px;
  overflow-x: auto;
}

.arrow {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  color: #64748b;
}

.actions {
  margin-top: 1.5rem;
  text-align: right;
}

button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #2563eb;
}
</style>
```

---

## Usage Flow

### 1. User Selects an Issue

When a user clicks on an issue in the dashboard:

```javascript
// In your issue list component
function handleIssueClick(issueId) {
  // Navigate to issue detail view
  router.push(`/issues/${issueId}`);

  // Or show recommendation in a modal
  showRecommendationModal(issueId);
}
```

### 2. Frontend Requests Recommendation

```javascript
// In your issue detail component
async function loadRecommendation() {
  try {
    const recommendation = await getRecommendation(issueId);
    setRecommendation(recommendation);
  } catch (error) {
    showError(error.message);
  }
}
```

### 3. Display Recommendation to User

```vue
<!-- In your template -->
<RecommendationView
  v-if="recommendation"
  :issue-id="issueId"
  @retry="loadRecommendation"
/>
```

---

## Testing the API

### Manual Testing with cURL

```bash
# Test with a known issue ID
curl http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000 | jq

# Force regenerate recommendation
curl "http://localhost:8000/api/v1/recommendations/550e8400-e29b-41d4-a716-446655440000?force_regenerate=true" | jq
```

### Expected Test Results

1. **Valid Issue ID**: Returns 200 OK with recommendation data
2. **Invalid Issue ID**: Returns 404 Not Found
3. **Missing WatsonX Credentials**: Returns 200 OK with `status: "mock"`
4. **Force Regenerate**: Returns fresh recommendation

---

## Mock Data for Development

### Sample Issue IDs for Testing

| Issue Type | Issue ID | Description |
|------------|----------|-------------|
| Accessibility | `550e8400-e29b-41d4-a716-446655440000` | Missing alt text |
| SEO | `6ba7b810-9dad-11d1-80b4-00c04fd430c8` | Missing meta description |
| Accessibility | `f47ac10b-58cc-4372-a567-0e02b2c3d479` | Multiple H1 tags |

### Sample Responses

**Missing Alt Text:**
```json
{
  "issue_id": "550e8400-e29b-41d4-a716-446655440000",
  "issue_type": "accessibility",
  "title": "Missing alt text on image",
  "plain_language_explanation": "Images need alternative text (alt text) so screen readers can describe them to visually impaired users. This is required by WCAG 2.1 and helps everyone understand your content.",
  "suggested_fix": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "before_snippet": "<img src='/hero.jpg'>",
  "after_snippet": "<img src='/hero.jpg' alt='Government building exterior with American flag'>",
  "confidence_score": 95.0,
  "model_used": "mock-fallback",
  "status": "mock"
}
```

**Missing Meta Description:**
```json
{
  "issue_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "issue_type": "seo",
  "title": "Missing meta description",
  "plain_language_explanation": "Meta descriptions appear in search results and help people decide whether to visit your page. They should be 150-160 characters and clearly describe what's on the page.",
  "suggested_fix": "<meta name='description' content='Brief, compelling description of this page that includes relevant keywords and encourages clicks (150-160 characters).'>",
  "before_snippet": "",
  "after_snippet": "<meta name='description' content='Brief, compelling description of this page that includes relevant keywords and encourages clicks (150-160 characters).'>",
  "confidence_score": 90.0,
  "model_used": "mock-fallback",
  "status": "mock"
}
```

---

## Implementation Notes

### 1. Error Handling

- Always handle errors gracefully
- Show user-friendly messages
- Provide retry options

```javascript
try {
  const recommendation = await getRecommendation(issueId);
  // Success
} catch (error) {
  // Show error to user
  showToast(`Failed to load recommendation: ${error.message}`);
  // Provide retry option
  showRetryButton();
}
```

### 2. Loading States

- Show loading indicators while waiting for AI
- Provide estimated time (2-3 seconds for mock, 5-10 seconds for real AI)

```vue
<div v-if="loading">
  <p>Generating AI recommendation...</p>
  <p>This usually takes 2-3 seconds</p>
  <div class="spinner"></div>
</div>
```

### 3. Confidence Indicators

- Highlight high-confidence recommendations
- Warn about low-confidence suggestions

```javascript
function getConfidenceText(score) {
  if (score >= 90) return "High Confidence";
  if (score >= 75) return "Medium Confidence";
  return "Low Confidence - Review Carefully";
}
```

### 4. Status Indicators

- Show whether using real AI or mock data
- Be transparent about demo mode

```vue
<span v-if="recommendation.status === 'mock'" class="demo-badge">
  Demo Mode
</span>
<span v-else class="ai-badge">
  AI Powered
</span>
```

---

## Integration Checklist

### Frontend Team

- [ ] Add API client function for recommendations
- [ ] Create RecommendationView component
- [ ] Add loading states
- [ ] Implement error handling
- [ ] Add confidence indicators
- [ ] Add status badges
- [ ] Test with mock data
- [ ] Test with real API
- [ ] Add copy-to-clipboard functionality
- [ ] Style the code comparison view

### Backend Team

- [ ] ✅ Implement recommendation endpoint
- [ ] ✅ Add mock responses
- [ ] ✅ Set up database models
- [ ] ✅ Add error handling
- [ ] ✅ Document API

### Testing

- [ ] Test with valid issue IDs
- [ ] Test with invalid issue IDs
- [ ] Test force_regenerate parameter
- [ ] Test error scenarios
- [ ] Test loading states
- [ ] Test UI display

---

## FAQ

### Q: What if WatsonX credentials aren't configured?

**A:** The API automatically falls back to mock responses. The `status` field will be `"mock"` instead of `"success"`. This is perfect for development and demos.

### Q: How long does it take to generate a recommendation?

**A:** Mock responses return instantly. Real WatsonX API calls take 5-10 seconds. The frontend should show a loading indicator.

### Q: Can we customize the mock responses?

**A:** Yes! The mock responses are in `src/backend/app/services/ai_service.py`. You can add more issue types or modify the existing ones.

### Q: What happens if we request a recommendation for the same issue multiple times?

**A:** The first request generates and stores the recommendation. Subsequent requests return the stored version unless you use `force_regenerate=true`.

### Q: How do we handle the "Bob makes the fix" requirement?

**A:** The API includes a `model_used` field that indicates whether it's using real AI or mock data. For the demo, we can show this as "IBM Bob helped generate this fix" when using mock responses.

---

## Next Steps

1. **Frontend Team**: Implement the API client and RecommendationView component
2. **Backend Team**: Test the endpoint with real issue data
3. **Product Team**: Verify the demo flow works end-to-end
4. **All Teams**: Test error scenarios and edge cases

The Recommendation API is ready for integration! Let's build the frontend components to bring this to life. 🚀
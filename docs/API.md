# PublicPulse AI - API Documentation

Complete API reference for the PublicPulse AI backend.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required (hackathon MVP). In production, implement JWT or API key authentication.

## Response Format

All responses follow this structure:

### Success Response
```json
{
  "data": { ... },
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error description",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "database": "connected",
  "features": {
    "ai_recommendations": true,
    "auto_fix_preview": true,
    "batch_processing": true
  }
}
```

---

## Scan Management

### POST /api/v1/scans

Initiate a new website scan.

**Request Body:**
```json
{
  "url": "https://example.gov",
  "max_pages": 50,
  "max_depth": 3
}
```

**Parameters:**
- `url` (required): Website URL to scan (must be valid HTTP/HTTPS URL)
- `max_pages` (optional): Maximum pages to scan (1-100, default: 50)
- `max_depth` (optional): Maximum crawl depth (1-5, default: 3)

**Response:** `201 Created`
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/scans \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.gov", "max_pages": 20}'
```

---

### GET /api/v1/scans/{scan_id}

Get current scan status (for polling).

**Path Parameters:**
- `scan_id` (required): UUID of the scan

**Response:** `200 OK`
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": 45,
  "pages_scanned": 12,
  "total_pages": 27,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:01:30Z",
  "error_message": null
}
```

**Status Values:**
- `pending`: Scan queued, not started yet
- `in_progress`: Currently scanning
- `completed`: Scan finished successfully
- `failed`: Scan encountered an error

**Example:**
```bash
curl http://localhost:8000/api/v1/scans/550e8400-e29b-41d4-a716-446655440000
```

---

### GET /api/v1/scans/{scan_id}/results

Get complete scan results (only available when status is `completed`).

**Path Parameters:**
- `scan_id` (required): UUID of the scan

**Response:** `200 OK`
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "domain_url": "https://example.gov",
  "status": "completed",
  "global_score": 75.5,
  "created_at": "2024-01-01T00:00:00Z",
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
      "detected_at": "2024-01-01T00:01:00Z"
    }
  ],
  "pages": [
    {
      "id": "page-uuid-1",
      "url": "https://example.gov/",
      "title": "Home - Example Government",
      "meta_description": "Official government website",
      "status_code": 200,
      "crawled_at": "2024-01-01T00:00:30Z"
    }
  ]
}
```

**Error Response:** `400 Bad Request` (if scan not completed)
```json
{
  "error": "Scan is not completed yet. Current status: in_progress"
}
```

---

### DELETE /api/v1/scans/{scan_id}

Delete a scan and all associated data.

**Path Parameters:**
- `scan_id` (required): UUID of the scan

**Response:** `204 No Content`

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/scans/550e8400-e29b-41d4-a716-446655440000
```

---

## Issue Management

### GET /api/v1/issues

Get list of issues with optional filters.

**Query Parameters:**
- `scan_id` (optional): Filter by scan ID
- `page_id` (optional): Filter by page ID
- `type` (optional): Filter by type (`seo`, `accessibility`, `qa`)
- `severity` (optional): Filter by severity (`high`, `medium`, `low`)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (1-100, default: 50)

**Response:** `200 OK`
```json
{
  "issues": [
    {
      "id": "issue-uuid-1",
      "page_id": "page-uuid-1",
      "type": "accessibility",
      "severity": "high",
      "title": "Missing alt text on image",
      "description": "Image at /hero.jpg is missing alternative text for screen readers",
      "priority_score": 95,
      "snippet": "<img src='/hero.jpg'>",
      "element_selector": "img.hero-image",
      "wcag_criterion": "1.1.1",
      "detected_at": "2024-01-01T00:01:00Z",
      "page_url": "https://example.gov/"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 50
}
```

**Example:**
```bash
# Get all high-severity accessibility issues
curl "http://localhost:8000/api/v1/issues?type=accessibility&severity=high"

# Get issues for specific scan
curl "http://localhost:8000/api/v1/issues?scan_id=550e8400-e29b-41d4-a716-446655440000"
```

---

### GET /api/v1/issues/priority

Get prioritized issues sorted by priority score.

**Query Parameters:**
- `scan_id` (optional): Filter by scan ID
- `limit` (optional): Number of top issues (1-50, default: 10)

**Response:** `200 OK`
```json
[
  {
    "id": "issue-uuid-1",
    "type": "accessibility",
    "severity": "high",
    "title": "Missing alt text on images",
    "priority_score": 95,
    "page_url": "https://example.gov/",
    "impact": "Critical accessibility barrier - prevents users with disabilities from accessing content"
  },
  {
    "id": "issue-uuid-2",
    "type": "seo",
    "severity": "high",
    "title": "Missing meta description",
    "priority_score": 90,
    "page_url": "https://example.gov/about",
    "impact": "Major SEO issue - significantly impacts search rankings and discoverability"
  }
]
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/issues/priority?limit=5"
```

---

### GET /api/v1/issues/{issue_id}

Get detailed information about a specific issue.

**Path Parameters:**
- `issue_id` (required): UUID of the issue

**Response:** `200 OK`
```json
{
  "id": "issue-uuid-1",
  "page_id": "page-uuid-1",
  "type": "accessibility",
  "severity": "high",
  "title": "Missing alt text on image",
  "description": "Image at /hero.jpg is missing alternative text for screen readers",
  "priority_score": 95,
  "snippet": "<img src='/hero.jpg' class='hero-image'>",
  "element_selector": "img.hero-image",
  "wcag_criterion": "1.1.1",
  "detected_at": "2024-01-01T00:01:00Z",
  "page_url": "https://example.gov/"
}
```

---

## Page Management

### GET /api/v1/pages

Get list of scanned pages.

**Query Parameters:**
- `scan_id` (optional): Filter by scan ID
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (1-100, default: 50)

**Response:** `200 OK`
```json
{
  "pages": [
    {
      "id": "page-uuid-1",
      "site_id": "scan-uuid-1",
      "url": "https://example.gov/",
      "title": "Home - Example Government",
      "meta_description": "Official government website",
      "meta_tags": {
        "og:title": "Example Government",
        "og:type": "website"
      },
      "h1_tags": ["Welcome to Example Government"],
      "status_code": 200,
      "load_time": 1.23,
      "crawled_at": "2024-01-01T00:00:30Z"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 50
}
```

---

### GET /api/v1/pages/{page_id}

Get detailed information about a specific page.

**Path Parameters:**
- `page_id` (required): UUID of the page

**Response:** `200 OK`
```json
{
  "id": "page-uuid-1",
  "site_id": "scan-uuid-1",
  "url": "https://example.gov/",
  "title": "Home - Example Government",
  "meta_description": "Official government website",
  "meta_tags": {
    "og:title": "Example Government",
    "og:type": "website",
    "twitter:card": "summary"
  },
  "h1_tags": ["Welcome to Example Government"],
  "status_code": 200,
  "load_time": 1.23,
  "crawled_at": "2024-01-01T00:00:30Z"
}
```

---

### GET /api/v1/pages/{page_id}/issues

Get all issues for a specific page.

**Path Parameters:**
- `page_id` (required): UUID of the page

**Response:** `200 OK`
```json
{
  "page_id": "page-uuid-1",
  "page_url": "https://example.gov/",
  "total_issues": 5,
  "issues": [
    {
      "id": "issue-uuid-1",
      "type": "accessibility",
      "severity": "high",
      "title": "Missing alt text",
      "description": "Image missing alternative text",
      "priority_score": 95
    }
  ]
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request (invalid input) |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limiting

Currently not implemented. In production, implement rate limiting:
- 60 requests per minute per IP
- 10 concurrent scans per user

## Pagination

All list endpoints support pagination:
- `page`: Page number (starts at 1)
- `page_size`: Items per page (max 100)

Response includes:
- `total`: Total number of items
- `page`: Current page
- `page_size`: Items per page

## Filtering

Issue endpoints support multiple filters that can be combined:

```bash
# Multiple filters
curl "http://localhost:8000/api/v1/issues?type=accessibility&severity=high&scan_id=xxx"
```

## Polling Best Practices

When polling for scan status:
1. Start with 2-second intervals
2. Increase to 5 seconds after 30 seconds
3. Stop polling when status is `completed` or `failed`
4. Implement exponential backoff for errors

Example polling logic:
```javascript
async function pollScanStatus(scanId) {
  let attempts = 0;
  const maxAttempts = 60; // 2 minutes max
  
  while (attempts < maxAttempts) {
    const response = await fetch(`/api/v1/scans/${scanId}`);
    const data = await response.json();
    
    if (data.status === 'completed' || data.status === 'failed') {
      return data;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    attempts++;
  }
  
  throw new Error('Scan timeout');
}
```

## WebSocket Support (Future)

For real-time updates, WebSocket support will be added:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/scans/{scan_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data.progress);
};
```

---

**For more information, see the [interactive API documentation](http://localhost:8000/docs)**
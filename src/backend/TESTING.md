# PublicPulse AI - Backend Testing Guide

This guide covers how to test the PublicPulse AI backend, verify the analysis engine, and prepare your changes for integration with the frontend and AI components.

## Setup & Environment

Ensure your virtual environment is active and all dependencies, including the headless browser, are installed.

```bash
cd src/backend
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser engines
playwright install chromium
```

## Running the Server

Start the FastAPI server with auto-reload enabled for development.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## Manual Testing Workflow

The backend uses a "Scan -> Poll -> Result" pattern. Follow these steps to verify the full flow:

### 1. Initiate a Scan
Using the Swagger UI (`POST /api/v1/scans`):
- **Request Body:**
  ```json
  {
    "url": "https://example.com",
    "max_pages": 5,
    "max_depth": 1
  }
  ```
- **Expected Output:** A `scan_id` (UUID).

### 2. Poll for Progress
Using the Swagger UI (`GET /api/v1/scans/{scan_id}`):
- Replace `{scan_id}` with your ID.
- **Expected Output:** `status` should move from `pending` -> `in_progress` -> `completed`.
- Verify `pages_scanned` increases as the crawler works.

### 3. Review Analysis Results
Using the Swagger UI (`GET /api/v1/scans/{scan_id}/results`):
- **Expected Output:** A full report including:
  - `global_score`: A quality score from 0-100.
  - `issues_by_type`: Counts of SEO vs Accessibility issues.
  - `top_issues`: The most critical problems found, with priority scores.
  - `pages`: List of URLs crawled.

---

## Automated Testing

We use `pytest` for automated logic verification.

### Running Tests
```bash
pytest src/backend/tests/ -v
```

### Adding New Tests
Create files in `src/backend/tests/test_*.py`. Example analyzer test:

```python
# src/backend/tests/test_analyzers.py
from app.analyzers.seo_analyzer import analyze_seo_issues

def test_missing_title_detection():
    page_data = {
        "url": "https://test.com",
        "title": "", # Missing title
        "h1_tags": ["Hello World"],
        "meta_description": "Description"
    }
    issues = analyze_seo_issues("test-page-id", page_data)
    assert any(issue.title == "Missing Page Title" for issue in issues)
```

---

## Integration Verification

Before handing over to the team, ensure these "contract" details are correct:

1.  **CORS:** Check `app/config.py` to ensure `cors_origins` includes `http://localhost:4321` (Astro default).
2.  **Database:** Verify `publicpulse.db` is updated correctly. You can use a SQLite viewer or the API to confirm data persistence.
3.  **JSON Schemas:** Ensure the output of `/api/v1/issues/priority` matches what the Frontend team expects (see `docs/API.md`).

---

## Shipping Changes

When your tests pass and you're ready to share with the team:

```bash
# 1. Create a feature branch
git checkout -b feat/backend-analysis-engine

# 2. Stage your new files
git add src/backend/app/analyzers/
git add src/backend/app/utils/
git add src/backend/app/routers/scans.py
git add src/backend/TESTING.md

# 3. Commit and push
git commit -m "feat: implement SEO/A11y analyzers and priority scoring engine"
git push origin feat/backend-analysis-engine
```
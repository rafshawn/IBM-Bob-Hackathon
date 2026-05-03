# Backend Development - Bob Sessions

## Role: Backend Engineer (Shawn)

### Goal
Build a reliable backend system that scans websites, generates structured issues, and stores results.

## Core Responsibilities

### 1. Async Task Management
- Implement a polling system so the frontend can track scan progress
- Use FastAPI BackgroundTasks for long-running operations
- Return UUID immediately, process in background

### 2. Human-Centric API
- Transform technical errors (e.g., `ARIA-01`) into human-readable labels (`Missing Image Description`)
- Provide business impact statements
- Return structured, consistent responses

### 3. Contextual Scraping
- Ensure the crawler grabs the `outerHTML` of failing elements
- Provide context for AI Engineer's prompts
- Capture sufficient surrounding HTML for analysis

### 4. Multi-Page Crawler (Playwright)
- Restrict crawling to same domain
- Extract key elements:
  - Title
  - Meta description
  - H1 tags
  - Images (alt text)
  - Links and navigation
  - ARIA attributes

### 5. Database Structure
Design and manage:
- **Sites**: Domain tracking and global scores
- **Pages**: Individual page data and metadata
- **Issues**: Detected problems with severity and priority
- **Recommendations**: AI-generated fixes (optional for backend)

### 6. API Endpoints

#### Scan Management
- `POST /api/v1/scans` - Initiate website scan
  - Input: `{ "url": "https://example.gov" }`
  - Output: `{ "scan_id": "uuid", "status": "pending" }`
  
- `GET /api/v1/scans/{scan_id}` - Get scan status
  - Output: `{ "scan_id": "uuid", "status": "in_progress", "progress": 45, "pages_scanned": 12 }`

- `GET /api/v1/scans/{scan_id}/results` - Get complete results
  - Output: Full scan data with all issues

#### Issue Management
- `GET /api/v1/issues` - List all issues
  - Query params: `?type=seo&severity=high&page_id=uuid`
  
- `GET /api/v1/issues/priority` - Get prioritized issues
  - Sorted by priority score

- `GET /api/v1/issues/{issue_id}` - Get specific issue
  - Include HTML snippet and context

#### Page Management
- `GET /api/v1/pages` - List scanned pages
  - Query params: `?site_id=uuid`
  
- `GET /api/v1/pages/{page_id}` - Get page details
  - Include all issues for that page

### 7. Priority Scoring Logic
- Severity-based scoring (High: 100, Medium: 50, Low: 25)
- Optional traffic weighting
- Impact on user experience
- WCAG compliance level

## Tech Stack

- **Framework**: FastAPI (async/await)
- **Database**: SQLite (SQLAlchemy ORM)
- **Crawler**: Playwright (async)
- **Validation**: Pydantic schemas
- **Testing**: pytest, pytest-asyncio

## Development Workflow

### Setting Up
```bash
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Running the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
pytest tests/ -v
pytest tests/test_crawler.py -v  # Specific test file
```

### Using IBM Bob

When working with Bob:
1. Provide context about the current task
2. Reference the project proposal for requirements
3. Ask for code reviews and suggestions
4. Document decisions and learnings in session files

## Session Documentation

Document your Bob sessions in this directory:
- `session_001_initial_setup.md` - Project setup and structure
- `session_002_crawler_implementation.md` - Crawler development
- `session_003_api_endpoints.md` - API implementation
- `session_004_database_optimization.md` - Performance tuning
- etc.

### Session Template

```markdown
# Session [Number]: [Title]

**Date**: YYYY-MM-DD
**Duration**: X hours
**Focus**: Brief description

## Objectives
- [ ] Objective 1
- [ ] Objective 2

## Work Completed
- Description of what was accomplished
- Code files created/modified
- Challenges encountered

## Decisions Made
- Technical decisions and rationale
- Trade-offs considered

## Next Steps
- What needs to be done next
- Blockers or dependencies

## Bob Interactions
- Key questions asked
- Helpful suggestions received
- Code snippets generated
```

## Integration Points

### With Frontend (Arvin)
- Ensure API responses match frontend expectations
- Provide clear error messages
- Support CORS for local development
- Document all endpoints with OpenAPI

### With AI Engineer (Moe)
- Provide issue context and HTML snippets
- Design recommendation storage structure
- Ensure issue IDs are consistent
- Support confidence scoring in database

### With Product Lead (Frank)
- Validate API design matches user flow
- Ensure demo scenarios work end-to-end
- Provide realistic test data
- Support priority use cases first

## Nice to Have Features

- Store crawl history for comparison
- Deduplicate pages (handle URL variations)
- Improve error handling and logging
- Rate limiting for crawler
- Retry logic for failed requests
- Webhook notifications for scan completion

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Playwright Python](https://playwright.dev/python/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Project Proposal](../../IBM%20Bob%20Hackathon%20-%20Project%20Proposal.md)

## Quick Reference

### Common Commands
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Start server with auto-reload
uvicorn app.main:app --reload

# Run tests with coverage
pytest --cov=app tests/

# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/
```

### Environment Variables
```
DATABASE_URL=sqlite:///./publicpulse.db
CORS_ORIGINS=http://localhost:3000,http://localhost:4321
MAX_CRAWL_DEPTH=3
MAX_PAGES_PER_SCAN=50
CRAWLER_TIMEOUT=30000
```

## Success Metrics

- [ ] Can scan a website and detect issues
- [ ] Issues are properly structured and stored
- [ ] API endpoints return correct data
- [ ] Background tasks work reliably
- [ ] Crawler respects domain boundaries
- [ ] Priority scoring is accurate
- [ ] API documentation is complete
- [ ] Tests cover critical paths

---

**Remember**: Focus on delivering a working MVP for the demo. Prioritize core functionality over nice-to-have features.
# PublicPulse AI - Backend

FastAPI-based backend for the PublicPulse AI website auditing platform.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 📁 Project Structure

```
src/backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database setup and session management
│   ├── models.py                # SQLAlchemy database models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── dependencies.py          # Shared dependencies
│   │
│   ├── routers/                 # API endpoint routers
│   │   ├── __init__.py
│   │   ├── scans.py            # Scan management endpoints
│   │   ├── issues.py           # Issue retrieval endpoints
│   │   └── pages.py            # Page data endpoints
│   │
│   ├── crawler/                 # Web crawling module
│   │   ├── __init__.py
│   │   └── playwright_crawler.py  # Playwright-based crawler
│   │
│   ├── analyzers/               # Issue detection (to be implemented)
│   │   ├── __init__.py
│   │   ├── seo_analyzer.py     # SEO issue detection
│   │   └── a11y_analyzer.py    # Accessibility checks
│   │
│   └── utils/                   # Utility functions (to be implemented)
│       ├── __init__.py
│       └── priority_scoring.py  # Priority calculation
│
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_api.py
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🗄️ Database

### Schema

The application uses SQLite by default (easily switchable to PostgreSQL).

**Tables:**
- `sites` - Scan sessions
- `pages` - Individual pages within a scan
- `issues` - Detected problems
- `recommendations` - AI-generated fixes

### Initialization

The database is automatically initialized on first run. To manually initialize:

```python
from app.database import init_db
init_db()
```

### Migrations (Future)

For production, use Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## 🔌 API Endpoints

### Health Check

```bash
GET /health
```

### Scan Management

```bash
# Start a new scan
POST /api/v1/scans
Body: {
  "url": "https://example.gov",
  "max_pages": 50,
  "max_depth": 3
}

# Get scan status (for polling)
GET /api/v1/scans/{scan_id}

# Get complete scan results
GET /api/v1/scans/{scan_id}/results

# Delete a scan
DELETE /api/v1/scans/{scan_id}
```

### Issue Management

```bash
# Get all issues (with filters)
GET /api/v1/issues?scan_id={id}&type=seo&severity=high

# Get prioritized issues
GET /api/v1/issues/priority?scan_id={id}&limit=10

# Get specific issue
GET /api/v1/issues/{issue_id}
```

### Page Management

```bash
# Get all pages
GET /api/v1/pages?scan_id={id}

# Get specific page
GET /api/v1/pages/{page_id}

# Get page issues
GET /api/v1/pages/{page_id}/issues
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py -v
```

## 🔧 Configuration

Configuration is managed through environment variables (`.env` file):

### Required Variables

```env
DATABASE_URL=sqlite:///./publicpulse.db
CORS_ORIGINS=http://localhost:3000,http://localhost:4321
```

### Optional Variables

```env
# Crawler settings
MAX_CRAWL_DEPTH=3
MAX_PAGES_PER_SCAN=50
CRAWLER_TIMEOUT=30000

# AI settings (for AI engineer)
WATSONX_API_KEY=your-key
WATSONX_PROJECT_ID=your-project-id

# Feature flags
ENABLE_AI_RECOMMENDATIONS=true
ENABLE_AUTO_FIX_PREVIEW=true
```

See `.env.example` for all available options.

## 🐛 Development

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/
```

### Adding New Endpoints

1. Create router in `app/routers/`
2. Define Pydantic schemas in `app/schemas.py`
3. Add database models if needed in `app/models.py`
4. Register router in `app/main.py`

Example:

```python
# app/routers/my_router.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-endpoint")
async def my_endpoint():
    return {"message": "Hello"}

# app/main.py
from app.routers import my_router

app.include_router(
    my_router.router,
    prefix="/api/v1/my",
    tags=["My Feature"]
)
```

## 🚀 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=false`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper logging
- [ ] Configure CORS for production domains
- [ ] Set up SSL/TLS
- [ ] Use production ASGI server (Gunicorn + Uvicorn)
- [ ] Set up monitoring and error tracking

### Production Server

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Playwright Python](https://playwright.dev/python/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contributing

This is a hackathon project. For development:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Document your changes
5. Submit for review

## 📝 Notes

### Current Status

✅ **Implemented:**
- FastAPI application structure
- Database models and schemas
- API endpoints (scans, issues, pages)
- Playwright crawler with domain restriction
- Background task system
- Configuration management

🚧 **To Be Implemented:**
- Issue detection logic (SEO, Accessibility)
- Priority scoring algorithm
- AI recommendation integration
- Comprehensive test suite
- Error handling improvements
- Logging system

### Known Issues

- Crawler is a basic implementation - needs optimization
- No rate limiting yet
- No caching implemented
- Test coverage is minimal

### Performance Considerations

- SQLite is fine for demo, but use PostgreSQL for production
- Consider adding Redis for caching
- Implement connection pooling for database
- Add request rate limiting
- Optimize crawler for large sites

## 🆘 Troubleshooting

### Playwright Installation Issues

```bash
# If playwright install fails, try:
python -m playwright install chromium
```

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm publicpulse.db
python -c "from app.database import init_db; init_db()"
```

### Import Errors

```bash
# Make sure you're in the backend directory and venv is activated
cd src/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

## 📞 Support

For questions or issues:
- Check the project proposal: `../../IBM Bob Hackathon - Project Proposal.md`
- Review Bob session notes: `../../bob_sessions/backend/`
- Consult with team members

---

**Built for the IBM Bob Hackathon** 🚀
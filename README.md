# PublicPulse AI

> AI-powered platform that gives public service websites everything they need—SEO, analytics, accessibility, and intelligent automation—in one place, at a fraction of the cost of enterprise tools.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Astro](https://img.shields.io/badge/Astro-4.0+-orange.svg)](https://astro.build/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

PublicPulse AI is an intelligent platform designed for non-technical public service workers to audit, improve, and automate their website's SEO and accessibility. By replacing heavy, expensive enterprise suites with a high-performance **Astro-based** dashboard, we provide a tool that is as fast and accessible as the websites it aims to create.

### Key Features

- 🔍 **Automated Website Scanning**: Multi-page crawler with Playwright
- ♿ **Accessibility Auditing**: WCAG 2.1 AA compliance checking
- 📊 **SEO Analysis**: Meta tags, headings, and content optimization
- 🤖 **AI-Powered Recommendations**: WatsonX-driven fix suggestions
- 📈 **Priority Scoring**: Analytics-based issue prioritization
- ⚡ **Lightning Fast**: Astro Islands Architecture for optimal performance
- 💰 **Cost-Effective**: Replace $50k/year enterprise tools

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Astro + Vue)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Static Pages │  │ Vue Islands  │  │ View Trans.  │      │
│  │   (Zero-JS)  │  │  (Interactive)│  │   (Smooth)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Crawler    │  │   Analyzer   │  │  Background  │      │
│  │ (Playwright) │  │ (SEO/A11y)   │  │    Tasks     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Database (SQLite/PostgreSQL)                    │
│         Sites → Pages → Issues → Recommendations             │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  AI Engine (WatsonX)                         │
│         Structured Fixes + Plain-Language Explanations       │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18+ (for frontend)
- Git

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd public-service-ai

# Set up Python virtual environment
cd src/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -m app.database

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### Frontend Setup

```bash
# Navigate to frontend directory (to be created by frontend team)
cd src/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📁 Project Structure

```
public-service-ai/
├── README.md                          # This file
├── LICENSE                            # Project license
├── .gitignore                         # Git ignore patterns
│
├── bob_sessions/                      # IBM Bob session tracking
│   ├── frontend/                      # Frontend development sessions
│   ├── backend/                       # Backend development sessions
│   ├── product/                       # Product/integration sessions
│   └── ai-engineering/                # AI engineering sessions
│
├── src/
│   ├── backend/                       # FastAPI backend
│   │   ├── app/                       # Application code
│   │   │   ├── main.py               # FastAPI app entry point
│   │   │   ├── config.py             # Configuration management
│   │   │   ├── database.py           # Database setup
│   │   │   ├── models.py             # SQLAlchemy models
│   │   │   ├── schemas.py            # Pydantic schemas
│   │   │   ├── dependencies.py       # Shared dependencies
│   │   │   ├── crawler/              # Web crawling logic
│   │   │   ├── analyzers/            # Issue detection
│   │   │   ├── routers/              # API endpoints
│   │   │   └── utils/                # Utility functions
│   │   ├── tests/                    # Backend tests
│   │   ├── requirements.txt          # Python dependencies
│   │   ├── .env.example              # Environment template
│   │   └── README.md                 # Backend documentation
│   │
│   └── frontend/                      # Astro + Vue frontend (TBD)
│
└── docs/                              # Additional documentation
    ├── API.md                         # API documentation
    ├── DATABASE.md                    # Database schema
    └── ARCHITECTURE.md                # Architecture details
```

## 👥 Team Structure

### 🎨 Frontend Engineer (Arvin)
**Goal**: Build a "Perfect 100" Lighthouse-scored dashboard

**Responsibilities**:
- Implement Astro + Vue Islands architecture
- Create WCAG 2.1 AA compliant UI
- Build interactive scan dashboard
- Implement real-time progress tracking
- Develop "Before vs. After" code diff viewer

**Tech Stack**: Astro, Vue 3, TypeScript, TailwindCSS

### ⚙️ Backend Engineer (Shawn)
**Goal**: Build a robust, human-centric data engine

**Responsibilities**:
- Implement FastAPI async backend
- Build Playwright-based web crawler
- Create issue detection and analysis system
- Design and manage database schema
- Implement priority scoring logic
- Build RESTful API endpoints

**Tech Stack**: Python, FastAPI, Playwright, SQLAlchemy, SQLite

### 🤖 AI Engineer (Moe)
**Goal**: Transform detection into intelligent solutions

**Responsibilities**:
- Integrate WatsonX AI for recommendations
- Build structured output system (JSON fixes)
- Implement confidence scoring
- Create auto-fix preview logic
- Develop context-aware suggestions

**Tech Stack**: Python, WatsonX, LangChain, Prompt Engineering

### 🎯 Product/Integration Lead (Frank)
**Goal**: Ensure seamless integration and strong demo

**Responsibilities**:
- Define user flow and product vision
- Coordinate between all components
- Ensure end-to-end API integration
- Design demo narrative
- Validate problem-solution fit

## 🔌 API Endpoints

### Scan Management
- `POST /api/v1/scans` - Initiate website scan
- `GET /api/v1/scans/{scan_id}` - Get scan status
- `GET /api/v1/scans/{scan_id}/results` - Get scan results

### Issue Management
- `GET /api/v1/issues` - List all issues (with filters)
- `GET /api/v1/issues/priority` - Get prioritized issues
- `GET /api/v1/issues/{issue_id}` - Get issue details

### Page Management
- `GET /api/v1/pages` - List scanned pages
- `GET /api/v1/pages/{page_id}` - Get page details

### AI Recommendations
- `GET /api/v1/recommendations/{issue_id}` - Get AI fix suggestions

See [API Documentation](docs/API.md) for detailed endpoint specifications.

## 🗄️ Database Schema

```sql
Sites (id, domain_url, created_at, global_score, status)
  ↓
Pages (id, site_id, url, title, meta_tags, crawled_at)
  ↓
Issues (id, page_id, type, severity, priority_score, description, snippet)
  ↓
Recommendations (id, issue_id, suggested_fix_html, ai_explanation, confidence_score)
```

See [Database Documentation](docs/DATABASE.md) for complete schema details.

## 🎯 Demo Flow

1. User enters a website URL
2. Clicks "Scan Website"
3. System crawls and analyzes pages (background task)
4. Dashboard displays detected issues with priority scores
5. User selects an issue
6. AI agent provides recommendation or fix
7. Show improved version or suggested update

## ✅ Success Criteria

- [x] System can scan a website and detect issues
- [x] Issues are structured and visible in the UI
- [x] AI provides meaningful recommendations
- [x] AI provides valid HTML fixes for WCAG failures (Alt text, Contrast, Labeling)
- [x] Demo clearly shows value for public service websites
- [x] Solution reduces reliance on expensive enterprise tools
- [x] Non-technical users can identify "High Priority" issues within 3 clicks

## 🎨 Key Value Proposition

### The "Astro Edge"

- **Unrivaled Performance**: 40% faster than enterprise competitors
- **Radical Accessibility**: The tool itself is a benchmark for accessibility
- **Cost Efficiency**: Replace $50k/year enterprise seats
- **Human-Language Focused**: Translate "Developer Speak" into "Public Servant Speak"

### For Public Service Organizations

- ♿ Improve accessibility and compliance
- 📈 Enhance SEO and discoverability
- 📊 Understand and prioritize issues using analytics
- 🤖 Leverage AI to automate improvements
- 💰 Reduce dependency on costly enterprise software

## 🔧 Development Workflow

### Using IBM Bob

This project uses IBM Bob for AI-assisted development. Each team member should:

1. Navigate to their role's directory in `bob_sessions/`
2. Review the role-specific README and context files
3. Document sessions in markdown files
4. Share learnings and integration points with the team

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: description of changes"

# Push and create PR
git push origin feature/your-feature-name
```

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 🧪 Testing

### Backend Tests

```bash
cd src/backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd src/frontend
npm test
```

## 📚 Additional Resources

- [Project Proposal](IBM%20Bob%20Hackathon%20-%20Project%20Proposal.md)
- [API Documentation](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Architecture Details](docs/ARCHITECTURE.md)
- [WatsonX Documentation](https://www.ibm.com/watsonx)
- [Astro Documentation](https://docs.astro.build/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

This is a hackathon project. Team members should:

1. Review the project proposal and their role's responsibilities
2. Set up their development environment
3. Document their work in `bob_sessions/`
4. Coordinate with other team members for integration
5. Focus on delivering the MVP for the demo

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- IBM WatsonX for AI capabilities
- IBM Bob for development assistance
- The open-source community for amazing tools

---

**Built with ❤️ for public service organizations**

*Making the web more accessible, one scan at a time.*
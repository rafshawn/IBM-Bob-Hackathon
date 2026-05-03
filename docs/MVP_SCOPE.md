# PublicPulse AI - MVP Scope

**Version:** 1.0  
**Target:** IBM Bob Hackathon Demo  
**Timeline:** May 2026  
**Status:** In Development

---

## MVP Philosophy

> **"Do one thing exceptionally well, then expand."**

Our MVP focuses on delivering a complete, working demonstration of the core value proposition: scan a website, detect issues, prioritize them, and provide AI-powered recommendations.

---

## In-Scope Features

### ✅ Core Functionality

#### 1. Website Scanning
- **Single-domain crawling** with Playwright
- **Multi-page support** (up to 50 pages)
- **Depth control** (max 3 levels)
- **Background task processing**
- **Real-time progress tracking**
- **Status polling** (pending → in_progress → completed)

**Technical Implementation:**
- FastAPI background tasks
- Playwright headless browser
- UUID-based scan tracking
- SQLite persistence

#### 2. Issue Detection
- **SEO Issues:**
  - Missing meta descriptions
  - Missing or duplicate titles
  - Missing H1 tags
  - Multiple H1 tags
  
- **Accessibility Issues:**
  - Missing alt text on images
  - Missing form labels
  - Low color contrast (basic detection)
  - Missing ARIA labels
  
- **Quality Assurance:**
  - Broken internal links
  - Missing page titles
  - Slow load times (>3s)

**Technical Implementation:**
- DOM parsing with Playwright
- Rule-based detection engine
- HTML snippet capture
- Element selector recording

#### 3. Priority Scoring
- **Severity-based scoring:**
  - High: 80-100 points
  - Medium: 40-79 points
  - Low: 0-39 points
  
- **Factors considered:**
  - Issue type (accessibility > SEO > QA)
  - WCAG compliance impact
  - Number of affected elements
  - Page importance (homepage weighted higher)

**Technical Implementation:**
- Algorithmic scoring in Python
- Stored in database
- Sortable in API responses

#### 4. AI Recommendations
- **WatsonX integration** for fix suggestions
- **Structured JSON output:**
  ```json
  {
    "suggested_fix_html": "<img src='...' alt='Description'>",
    "ai_explanation": "Plain language explanation",
    "confidence_score": 95.0,
    "reasoning": "Why this fix works"
  }
  ```
- **Confidence scoring** (0-100)
- **Before/after snippets**

**Technical Implementation:**
- WatsonX API integration
- Prompt engineering for structured output
- Context-aware recommendations
- Fallback for API failures

#### 5. Dashboard Interface
- **Scan initiation form:**
  - URL input with validation
  - Max pages selector
  - Max depth selector
  
- **Progress indicator:**
  - Real-time status updates
  - Pages scanned counter
  - Estimated time remaining
  
- **Results dashboard:**
  - Global quality score
  - Issue breakdown by type
  - Issue breakdown by severity
  - Top 10 priority issues
  
- **Issue detail view:**
  - Full issue description
  - Affected page URL
  - HTML snippet
  - Element selector
  - WCAG criterion (if applicable)
  
- **AI recommendation view:**
  - Request recommendation button
  - Before/after code comparison
  - Plain-language explanation
  - Confidence score indicator

**Technical Implementation:**
- Astro for static shell
- Vue Islands for interactive components
- TailwindCSS for styling
- View Transitions API for smooth navigation

#### 6. RESTful API
- **Scan Management:**
  - `POST /api/v1/scans` - Initiate scan
  - `GET /api/v1/scans/{scan_id}` - Get status
  - `GET /api/v1/scans/{scan_id}/results` - Get results
  
- **Issue Management:**
  - `GET /api/v1/issues` - List issues (with filters)
  - `GET /api/v1/issues/priority` - Get prioritized issues
  - `GET /api/v1/issues/{issue_id}` - Get issue details
  
- **Page Management:**
  - `GET /api/v1/pages` - List pages
  - `GET /api/v1/pages/{page_id}` - Get page details
  - `GET /api/v1/pages/{page_id}/issues` - Get page issues

**Technical Implementation:**
- FastAPI with async/await
- Pydantic schemas for validation
- SQLAlchemy ORM
- Comprehensive error handling

---

## Out-of-Scope (Post-MVP)

### 🚫 Not in Hackathon Demo

#### User Management
- Authentication/authorization
- User accounts
- Team collaboration
- Role-based access control

**Rationale:** Adds complexity without demonstrating core value

#### Historical Tracking
- Scan history
- Trend analysis
- Issue resolution tracking
- Before/after comparisons over time

**Rationale:** Requires time-series data and complex UI

#### Advanced Analytics
- Traffic-weighted prioritization
- Google Analytics integration
- Custom scoring algorithms
- Predictive insights

**Rationale:** Needs external data sources and ML models

#### Scheduled Scans
- Automated recurring scans
- Cron-based scheduling
- Email notifications
- Webhook integrations

**Rationale:** Infrastructure complexity for demo

#### Export Features
- PDF reports
- CSV exports
- Custom report templates
- White-label branding

**Rationale:** Not essential for value demonstration

#### Advanced AI Features
- Auto-fix application
- Bulk fix suggestions
- Learning from user feedback
- Custom AI models

**Rationale:** Requires more AI engineering time

#### Mobile App
- Native iOS/Android apps
- Progressive Web App
- Offline support

**Rationale:** Web-first approach sufficient for MVP

#### Integrations
- CMS plugins (WordPress, Drupal)
- CI/CD pipeline integration
- Slack/Teams notifications
- GitHub Actions

**Rationale:** Requires partner ecosystem development

---

## Technical Constraints

### Performance Targets
- **Scan initiation:** < 500ms response time
- **Page crawling:** 2-5 pages per second
- **Issue detection:** < 100ms per page
- **AI recommendations:** < 3 seconds per issue
- **Dashboard load:** < 1 second (Lighthouse 100)

### Scalability Limits (MVP)
- **Max pages per scan:** 50
- **Max crawl depth:** 3 levels
- **Concurrent scans:** 5
- **Database:** SQLite (single file)
- **No caching layer**

### Browser Support
- **Modern browsers only:**
  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+

### Accessibility Compliance
- **WCAG 2.1 AA** for the dashboard itself
- **Keyboard navigation** fully supported
- **Screen reader compatible**
- **Color contrast** meets standards

---

## Data Model (MVP)

### Database Tables

```
Sites (scan sessions)
├── id (UUID)
├── domain_url
├── status (pending|in_progress|completed|failed)
├── global_score
├── created_at
└── updated_at

Pages (crawled pages)
├── id (UUID)
├── site_id (FK)
├── url
├── title
├── meta_description
├── meta_tags (JSON)
├── h1_tags (JSON)
└── crawled_at

Issues (detected problems)
├── id (UUID)
├── page_id (FK)
├── type (seo|accessibility|qa)
├── severity (high|medium|low)
├── priority_score
├── title
├── description
├── snippet
├── element_selector
├── wcag_criterion
└── detected_at

Recommendations (AI fixes)
├── id (UUID)
├── issue_id (FK)
├── suggested_fix_html
├── ai_explanation
├── confidence_score
├── before_snippet
├── after_snippet
└── created_at
```

---

## User Stories (MVP)

### Story 1: Scan a Website
**As a** public service web admin  
**I want to** scan my website for issues  
**So that** I can understand what needs improvement

**Acceptance Criteria:**
- ✅ Can enter a valid URL
- ✅ Can start a scan with one click
- ✅ See real-time progress
- ✅ Receive results when complete

### Story 2: View Prioritized Issues
**As a** non-technical user  
**I want to** see issues sorted by priority  
**So that** I know what to fix first

**Acceptance Criteria:**
- ✅ Issues displayed with priority scores
- ✅ Can filter by type (SEO/Accessibility/QA)
- ✅ Can filter by severity (High/Medium/Low)
- ✅ Top 10 issues highlighted

### Story 3: Understand an Issue
**As a** web admin  
**I want to** see detailed information about an issue  
**So that** I understand what's wrong and where

**Acceptance Criteria:**
- ✅ Click issue to see details
- ✅ View affected page URL
- ✅ See HTML snippet
- ✅ Read plain-language description
- ✅ Understand business impact

### Story 4: Get AI Recommendation
**As a** non-technical user  
**I want to** get an AI-powered fix suggestion  
**So that** I know how to resolve the issue

**Acceptance Criteria:**
- ✅ Request recommendation with one click
- ✅ See before/after code comparison
- ✅ Read plain-language explanation
- ✅ View confidence score
- ✅ Copy suggested fix

---

## Success Criteria

### Functional Requirements
- [x] System can scan a multi-page website
- [x] Issues are detected and categorized
- [x] Priority scoring works correctly
- [x] AI provides valid HTML fixes
- [x] Dashboard displays results clearly
- [x] API endpoints function as documented

### Non-Functional Requirements
- [ ] Dashboard achieves Lighthouse 100 score
- [ ] Dashboard meets WCAG 2.1 AA standards
- [ ] API response times < 500ms
- [ ] Scan completes in < 5 minutes for 25 pages
- [ ] Zero critical bugs in demo

### Demo Requirements
- [ ] Can scan example.gov successfully
- [ ] Detects at least 10 issues
- [ ] AI provides 3+ valid recommendations
- [ ] Non-technical user can navigate in < 3 clicks
- [ ] Demo runs smoothly without errors

---

## Testing Strategy

### Unit Tests
- **Backend:** pytest for core logic
- **Frontend:** Vitest for Vue components
- **Coverage target:** 70%+

### Integration Tests
- API endpoint testing
- Database operations
- Crawler functionality
- AI integration

### Manual Testing
- End-to-end user flows
- Cross-browser compatibility
- Accessibility testing (screen readers)
- Performance testing

### Demo Rehearsal
- Full walkthrough 3x before presentation
- Backup demo data prepared
- Fallback plan if live demo fails

---

## Deployment Strategy

### Development Environment
- Local SQLite database
- Local FastAPI server (port 8000)
- Local Astro dev server (port 4321)
- Environment variables in .env

### Demo Environment
- Hosted backend (Railway/Render)
- Hosted frontend (Vercel/Netlify)
- PostgreSQL database (if needed)
- Environment variables configured

### Fallback Plan
- Pre-recorded demo video
- Static screenshots
- Prepared demo data
- Localhost demo as backup

---

## Risk Mitigation

### Technical Risks

**Risk:** Crawler fails on complex sites  
**Mitigation:** Test on multiple public service sites, implement robust error handling

**Risk:** AI API rate limits or failures  
**Mitigation:** Implement caching, fallback responses, mock data for demo

**Risk:** Performance issues with large scans  
**Mitigation:** Limit to 50 pages, implement timeouts, show progress

**Risk:** Database corruption  
**Mitigation:** Regular backups, transaction management, data validation

### Demo Risks

**Risk:** Live demo fails  
**Mitigation:** Pre-recorded video, static screenshots, localhost backup

**Risk:** Network issues  
**Mitigation:** Localhost demo, cached data, offline mode

**Risk:** Time constraints  
**Mitigation:** Scripted demo (5 minutes), focus on key features

---

## Development Timeline

### Week 1: Foundation
- [x] Backend API structure
- [x] Database schema
- [x] Basic crawler
- [x] Frontend scaffold

### Week 2: Core Features
- [x] Issue detection logic
- [x] Priority scoring
- [x] API endpoints
- [ ] Dashboard UI

### Week 3: AI Integration
- [ ] WatsonX integration
- [ ] Recommendation engine
- [ ] Confidence scoring
- [ ] UI for recommendations

### Week 4: Polish & Demo
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Demo preparation
- [ ] Documentation

---

## Definition of Done

A feature is "done" when:
- ✅ Code is written and tested
- ✅ Unit tests pass
- ✅ Integration tests pass
- ✅ Documentation is updated
- ✅ Code is reviewed
- ✅ Works in demo environment
- ✅ Meets acceptance criteria

---

## Post-MVP Roadmap Preview

### Phase 2: Enhanced Intelligence
- Historical tracking
- Trend analysis
- Scheduled scans
- Email notifications

### Phase 3: Collaboration
- User accounts
- Team features
- Role-based access
- Shared dashboards

### Phase 4: Enterprise
- Advanced analytics
- Custom integrations
- White-label option
- On-premise deployment

---

## Key Metrics to Track

### During Development
- Features completed vs. planned
- Bugs found and fixed
- Test coverage percentage
- API response times

### During Demo
- Audience engagement
- Questions asked
- Feature requests
- Positive feedback

### Post-Demo
- Interest from organizations
- Beta signup requests
- Partnership inquiries
- Media coverage

---

## Team Responsibilities

### Frontend (Arvin)
- Dashboard UI implementation
- Vue Islands for interactivity
- Lighthouse 100 optimization
- WCAG 2.1 AA compliance

### Backend (Shawn)
- API endpoints
- Crawler implementation
- Issue detection logic
- Database management

### AI Engineering (Moe)
- WatsonX integration
- Recommendation engine
- Prompt engineering
- Confidence scoring

### Product/Integration (Frank)
- Feature coordination
- Demo script
- Integration testing
- Documentation

---

## Conclusion

This MVP scope is designed to deliver a compelling demonstration of PublicPulse AI's core value proposition while remaining achievable within hackathon constraints. By focusing on essential features and deferring complexity, we can build a solid foundation for future growth.

**Remember:** It's better to have 5 features that work perfectly than 20 features that work poorly.

---

**Related Documents:**
- [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md) - Overall product vision
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - Presentation guide
- [API.md](API.md) - Technical API documentation
- [DATABASE.md](DATABASE.md) - Database schema details
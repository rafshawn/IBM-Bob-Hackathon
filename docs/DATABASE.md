# PublicPulse AI - Database Schema

Complete database schema documentation for PublicPulse AI.

## Database Technology

- **Development**: SQLite (file-based, no setup required)
- **Production**: PostgreSQL (recommended for scalability)

## Connection String

```python
# SQLite (default)
DATABASE_URL = "sqlite:///./publicpulse.db"

# PostgreSQL (production)
DATABASE_URL = "postgresql://user:password@localhost:5432/publicpulse"
```

## Schema Overview

```
Sites (scan sessions)
  ↓ has many
Pages (individual URLs)
  ↓ has many
Issues (detected problems)
  ↓ has many
Recommendations (AI-generated fixes)
```

## Entity Relationship Diagram

```mermaid
erDiagram
    SITES ||--o{ PAGES : contains
    PAGES ||--o{ ISSUES : has
    ISSUES ||--o{ RECOMMENDATIONS : generates
    
    SITES {
        string id PK "UUID"
        string domain_url "Base URL"
        datetime created_at
        datetime updated_at
        string status "pending|in_progress|completed|failed"
        float global_score "Overall quality score"
        int total_pages "Expected pages"
        int pages_scanned "Completed pages"
        text error_message "Error details if failed"
    }
    
    PAGES {
        string id PK "UUID"
        string site_id FK
        string url "Full page URL"
        string title "Page title"
        text meta_description
        json meta_tags "All meta tags"
        json h1_tags "List of H1 headings"
        datetime crawled_at
        int status_code "HTTP status"
        float load_time "Page load time in seconds"
    }
    
    ISSUES {
        string id PK "UUID"
        string page_id FK
        string type "seo|accessibility|qa"
        string severity "high|medium|low"
        int priority_score "0-100"
        string title "Short description"
        text description "Detailed explanation"
        text snippet "HTML snippet"
        string element_selector "CSS selector"
        string wcag_criterion "e.g., 1.1.1"
        datetime detected_at
    }
    
    RECOMMENDATIONS {
        string id PK "UUID"
        string issue_id FK
        text suggested_fix_html "Corrected HTML"
        text ai_explanation "Plain language explanation"
        float confidence_score "0-100"
        text reasoning "Why this fix works"
        text before_snippet "Original HTML"
        text after_snippet "Fixed HTML"
        text diff_html "Visual diff"
        datetime created_at
        string model_used "AI model identifier"
    }
```

## Table Definitions

### Sites Table

Represents a website scan session.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID identifier |
| domain_url | VARCHAR(255) | NOT NULL, INDEX | Base URL of the website |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | When scan was initiated |
| updated_at | DATETIME | DEFAULT NOW | Last update timestamp |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Current scan status |
| global_score | FLOAT | NULL | Overall quality score (0-100) |
| total_pages | INTEGER | DEFAULT 0 | Expected number of pages |
| pages_scanned | INTEGER | DEFAULT 0 | Number of pages completed |
| error_message | TEXT | NULL | Error details if scan failed |

**Status Values:**
- `pending`: Scan queued, not started
- `in_progress`: Currently scanning
- `completed`: Scan finished successfully
- `failed`: Scan encountered an error

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `domain_url`
- INDEX on `status`

**Example:**
```sql
INSERT INTO sites (id, domain_url, status, created_at)
VALUES ('550e8400-e29b-41d4-a716-446655440000', 'https://example.gov', 'pending', NOW());
```

---

### Pages Table

Represents individual pages within a scanned site.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID identifier |
| site_id | VARCHAR(36) | FOREIGN KEY, NOT NULL, INDEX | Reference to sites table |
| url | VARCHAR(512) | NOT NULL, INDEX | Full page URL |
| title | VARCHAR(255) | NULL | Page title from `<title>` tag |
| meta_description | TEXT | NULL | Meta description content |
| meta_tags | JSON | NULL | All meta tags as JSON object |
| h1_tags | JSON | NULL | Array of H1 heading texts |
| crawled_at | DATETIME | DEFAULT NOW | When page was crawled |
| status_code | INTEGER | NULL | HTTP status code (200, 404, etc.) |
| load_time | FLOAT | NULL | Page load time in seconds |

**Relationships:**
- `site_id` → `sites.id` (CASCADE DELETE)

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY INDEX on `site_id`
- INDEX on `url`

**Example:**
```sql
INSERT INTO pages (id, site_id, url, title, meta_description, status_code)
VALUES (
  '660e8400-e29b-41d4-a716-446655440001',
  '550e8400-e29b-41d4-a716-446655440000',
  'https://example.gov/',
  'Home - Example Government',
  'Official government website',
  200
);
```

---

### Issues Table

Represents detected problems on pages.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID identifier |
| page_id | VARCHAR(36) | FOREIGN KEY, NOT NULL, INDEX | Reference to pages table |
| type | VARCHAR(20) | NOT NULL, INDEX | Issue category |
| severity | VARCHAR(10) | NOT NULL, INDEX | Issue severity level |
| priority_score | INTEGER | NOT NULL, INDEX | Priority ranking (0-100) |
| title | VARCHAR(255) | NOT NULL | Short issue description |
| description | TEXT | NOT NULL | Detailed explanation |
| snippet | TEXT | NULL | HTML snippet showing the issue |
| element_selector | VARCHAR(255) | NULL | CSS selector for the element |
| wcag_criterion | VARCHAR(10) | NULL | WCAG success criterion |
| detected_at | DATETIME | DEFAULT NOW | When issue was detected |

**Type Values:**
- `seo`: Search engine optimization issues
- `accessibility`: WCAG accessibility violations
- `qa`: Quality assurance issues

**Severity Values:**
- `high`: Critical issues requiring immediate attention
- `medium`: Important issues to address soon
- `low`: Minor improvements

**Relationships:**
- `page_id` → `pages.id` (CASCADE DELETE)

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY INDEX on `page_id`
- INDEX on `type`
- INDEX on `severity`
- INDEX on `priority_score` (for sorting)

**Example:**
```sql
INSERT INTO issues (
  id, page_id, type, severity, priority_score,
  title, description, snippet, wcag_criterion
)
VALUES (
  '770e8400-e29b-41d4-a716-446655440002',
  '660e8400-e29b-41d4-a716-446655440001',
  'accessibility',
  'high',
  95,
  'Missing alt text on image',
  'Image at /hero.jpg is missing alternative text for screen readers',
  '<img src="/hero.jpg" class="hero-image">',
  '1.1.1'
);
```

---

### Recommendations Table

Represents AI-generated recommendations for fixing issues.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID identifier |
| issue_id | VARCHAR(36) | FOREIGN KEY, NOT NULL, INDEX | Reference to issues table |
| suggested_fix_html | TEXT | NOT NULL | Corrected HTML code |
| ai_explanation | TEXT | NOT NULL | Plain language explanation |
| confidence_score | FLOAT | NOT NULL | AI confidence (0-100) |
| reasoning | TEXT | NULL | Why this fix is recommended |
| before_snippet | TEXT | NULL | Original HTML |
| after_snippet | TEXT | NULL | Fixed HTML |
| diff_html | TEXT | NULL | Visual diff for display |
| created_at | DATETIME | DEFAULT NOW | When recommendation was generated |
| model_used | VARCHAR(50) | NULL | AI model identifier |

**Relationships:**
- `issue_id` → `issues.id` (CASCADE DELETE)

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY INDEX on `issue_id`

**Example:**
```sql
INSERT INTO recommendations (
  id, issue_id, suggested_fix_html, ai_explanation, confidence_score
)
VALUES (
  '880e8400-e29b-41d4-a716-446655440003',
  '770e8400-e29b-41d4-a716-446655440002',
  '<img src="/hero.jpg" alt="Government building exterior" class="hero-image">',
  'Added descriptive alt text that explains what the image shows. This helps screen reader users understand the visual content.',
  95.0
);
```

---

## Common Queries

### Get all issues for a scan

```sql
SELECT i.*, p.url as page_url
FROM issues i
JOIN pages p ON i.page_id = p.id
WHERE p.site_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY i.priority_score DESC;
```

### Get high-priority accessibility issues

```sql
SELECT i.*, p.url as page_url
FROM issues i
JOIN pages p ON i.page_id = p.id
WHERE i.type = 'accessibility'
  AND i.severity = 'high'
ORDER BY i.priority_score DESC
LIMIT 10;
```

### Get scan statistics

```sql
SELECT 
  s.id,
  s.domain_url,
  s.status,
  COUNT(DISTINCT p.id) as total_pages,
  COUNT(i.id) as total_issues,
  SUM(CASE WHEN i.severity = 'high' THEN 1 ELSE 0 END) as high_severity_issues,
  SUM(CASE WHEN i.type = 'accessibility' THEN 1 ELSE 0 END) as accessibility_issues
FROM sites s
LEFT JOIN pages p ON s.id = p.site_id
LEFT JOIN issues i ON p.id = i.page_id
WHERE s.id = '550e8400-e29b-41d4-a716-446655440000'
GROUP BY s.id;
```

### Get pages with most issues

```sql
SELECT 
  p.url,
  p.title,
  COUNT(i.id) as issue_count,
  SUM(CASE WHEN i.severity = 'high' THEN 1 ELSE 0 END) as high_issues
FROM pages p
LEFT JOIN issues i ON p.id = i.page_id
WHERE p.site_id = '550e8400-e29b-41d4-a716-446655440000'
GROUP BY p.id
ORDER BY issue_count DESC
LIMIT 10;
```

## Migrations

### Initial Schema Creation

```sql
-- Create sites table
CREATE TABLE sites (
    id VARCHAR(36) PRIMARY KEY,
    domain_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    global_score FLOAT,
    total_pages INTEGER DEFAULT 0,
    pages_scanned INTEGER DEFAULT 0,
    error_message TEXT,
    INDEX idx_domain (domain_url),
    INDEX idx_status (status)
);

-- Create pages table
CREATE TABLE pages (
    id VARCHAR(36) PRIMARY KEY,
    site_id VARCHAR(36) NOT NULL,
    url VARCHAR(512) NOT NULL,
    title VARCHAR(255),
    meta_description TEXT,
    meta_tags JSON,
    h1_tags JSON,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER,
    load_time FLOAT,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    INDEX idx_site (site_id),
    INDEX idx_url (url)
);

-- Create issues table
CREATE TABLE issues (
    id VARCHAR(36) PRIMARY KEY,
    page_id VARCHAR(36) NOT NULL,
    type VARCHAR(20) NOT NULL,
    severity VARCHAR(10) NOT NULL,
    priority_score INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    snippet TEXT,
    element_selector VARCHAR(255),
    wcag_criterion VARCHAR(10),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE,
    INDEX idx_page (page_id),
    INDEX idx_type (type),
    INDEX idx_severity (severity),
    INDEX idx_priority (priority_score)
);

-- Create recommendations table
CREATE TABLE recommendations (
    id VARCHAR(36) PRIMARY KEY,
    issue_id VARCHAR(36) NOT NULL,
    suggested_fix_html TEXT NOT NULL,
    ai_explanation TEXT NOT NULL,
    confidence_score FLOAT NOT NULL,
    reasoning TEXT,
    before_snippet TEXT,
    after_snippet TEXT,
    diff_html TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_used VARCHAR(50),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    INDEX idx_issue (issue_id)
);
```

## Data Integrity

### Cascade Deletes

When a site is deleted:
1. All associated pages are deleted
2. All issues on those pages are deleted
3. All recommendations for those issues are deleted

This is handled automatically by the `ON DELETE CASCADE` foreign key constraints.

### Constraints

- All IDs are UUIDs (36 characters)
- URLs are validated before insertion
- Status values are restricted to defined enums
- Timestamps are automatically managed

## Performance Considerations

### Indexes

Critical indexes for performance:
- `sites.domain_url` - For looking up scans by domain
- `pages.site_id` - For joining pages to sites
- `issues.page_id` - For joining issues to pages
- `issues.priority_score` - For sorting by priority
- `issues.type` and `issues.severity` - For filtering

### Query Optimization

- Use `LIMIT` for large result sets
- Add indexes on frequently filtered columns
- Use `JOIN` instead of subqueries when possible
- Consider materialized views for complex aggregations

### Scaling

For large deployments:
- Partition tables by date
- Archive old scans
- Use read replicas for reporting
- Implement caching layer (Redis)

## Backup and Maintenance

### Backup Strategy

```bash
# SQLite backup
cp publicpulse.db publicpulse.db.backup

# PostgreSQL backup
pg_dump publicpulse > backup.sql
```

### Cleanup Old Data

```sql
-- Delete scans older than 30 days
DELETE FROM sites 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

## Future Enhancements

Planned schema additions:
- `users` table for authentication
- `scan_history` for tracking changes over time
- `notifications` for alerting on critical issues
- `api_keys` for API access control
- `webhooks` for event notifications

---

**For implementation details, see `src/backend/app/models.py`**
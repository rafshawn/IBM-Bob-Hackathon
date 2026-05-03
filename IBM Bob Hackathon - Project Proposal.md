# Project Proposal

# Project Proposal: PublicPulse AI

AI-powered platform that gives public service websites everything they need—SEO, analytics, accessibility, and intelligent automation—in one place, at a fraction of the cost of enterprise tools.

The platform scans websites, identifies issues, prioritizes them using analytics, and uses AI agents to recommend or simulate fixes.

The goal is to replace expensive enterprise tools with a unified, intelligent, and cost-effective solution.

## Project Description

\_\_\_ is an intelligent platform designed for non-technical public service workers to audit, improve, and automate their website’s SEO and accessibility. By replacing heavy, expensive enterprise suites with a high-performance **Astro-based** dashboard, we provide a tool that is as fast and accessible as the websites it aims to create.

## System Architecture

The idea is to utilise an **Islands Architecture** instead of a SPA app architecture. This ensures the dashboard is lightweight and accessible, even on older hardware common in public sectors.

* **Frontend (Astro \+ Vue Islands):**  
  * **Static/SSR Layer:** Astro handles the shell, navigation, and educational content (Zero-JS).  
  * **Interactive Islands:** Vue components for the "Scan Input," "Real-time Progress," and "AI Fix Preview."  
* **Backend (FastAPI):** Asynchronous engine managing the crawler and AI requests.  
* **Crawler (Playwright):** Deep-scans DOM elements and captures HTML snippets for AI context.  
* **AI Engine (watsonx / LLM):** Generates structured JSON fixes and plain-language explanations.  
* **Database (PostgreSQL/SQLite):** Stores site hierarchies, historical metrics, and AI confidence scores.

## Key Value Proposition (The "Astro Edge")

* **Unrivaled Performance:** By using Astro, our platform loads up to 40% faster than enterprise competitors, working flawlessly on low-bandwidth public sector networks.  
* **Radical Accessibility:** We don't just fix accessibility; our tool is a benchmark for it.  
* **Cost Efficiency:** Replacing $50k/year enterprise seats with a lean, AI-driven alternative.  
* **Human-Language Focused:** We translate "Developer Speak" into "Public Servant Speak."

# Demo Flow

1. User enters a website URL  
2. Clicks “Scan Website”  
3. System crawls and analyzes pages  
4. Dashboard displays detected issues  
5. User selects an issue  
6. AI agent provides recommendation or fix  
7. Show improved version or suggested update

# Success Criteria

* The system can scan a website and detect issues  
* Issues are structured and visible in the UI  
* AI provides meaningful recommendations  
  * The AI provides a valid HTML fix for at least 3 common WCAG failures (Alt text, Contrast, Labeling).  
* The demo clearly shows value for public service websites  
* The solution reduces reliance on expensive enterprise tools  
* A non-technical user can identify and understand a "High Priority" issue within 3 clicks.

# Key Value Proposition

This platform enables public service organizations to:

* Improve accessibility and compliance  
* Enhance SEO and discoverability  
* Understand and prioritize issues using analytics  
* Leverage AI to automate improvements  
* Reduce dependency on costly enterprise software

# Product Strategy (Frank)

## Product / Integration Lead

### Goal

Ensure all components work together and deliver a strong, clear demo.

### Responsibilities

* Define user flow and product vision  
* Coordinate between frontend, backend, and AI components  
* Ensure API integration works end-to-end  
* Design demo narrative and presentation  
* Validate that the system solves the intended problem

# Frontend Strategy (Arvin)

## Frontend Engineer

### Goal

Build a clean, simple, and demo-ready dashboard that displays issues and allows users to trigger scans.

### Core Responsibilities

Build a "Perfect 100" Lighthouse-scored dashboard.

* Implement **Hybrid Rendering**: SSR for scan results, SSG for documentation.  
* Develop **Vue Islands** for complex UI (e.g., the interactive "Before vs. After" code diff).  
* Utilize **View Transitions API** to create smooth, app-like navigation without the weight of an SPA.  
* Create main dashboard displaying issues  
  * Ensure the dashboard itself meets **WCAG 2.1 AA** standards.  
* Build input field for URL and “Scan Website” button  
* Display issue table with:  
  * Type (SEO, Accessibility, QA)  
  * Severity (High, Medium, Low)  
  * Priority score  
* Implement page-level view (click a page → see its issues)

### Nice to Have

* Filters (SEO / Accessibility / QA)  
* Status badges for severity levels  
* Basic styling for better presentation

### Deliverable

A working UI that allows users to scan a site and visualize prioritized issues.

### Tech Stack

* Astro \+ Vue  
* Design resources:  
  * [https://getdesign.md/](https://getdesign.md/)

Public service workers often use older hardware or restricted networks. Astro’s **"Zero-JS"** default is a massive accessibility feature in itself.

* **Lighthouse Scores:** You will likely hit **100/100** on Performance and Accessibility out of the box. Enterprise tools like *Siteimprove* or *Ahrefs* are heavy SPAs that can feel sluggish; your tool will feel like a native part of the browser.  
* **A11y First:** Astro encourages using standard HTML `<a>` and `<button>` tags rather than complex JS-based routing. This makes your platform inherently more compatible with screen readers.

# Backend Strategy (Shawn)

## Backend Engineer

### Goal

Build a reliable backend system that scans websites, generates structured issues, and stores results.

### Core Responsibilities

Build a robust, human-centric data engine.

* **Async Task Management:** Implement a polling system so the frontend can track scan progress.  
* **Human-Centric API:** Transform technical errors (e.g., `ARIA-01`) into human-readable labels (`Missing Image Description`) and business impact statements.  
* **Contextual Scrapping:** Ensure the crawler grabs the `outerHTML` of failing elements to feed the AI Engineer’s prompts.  
* Implement multi-page crawler (Playwright)  
* Restrict crawling to same domain  
* Extract key elements:  
  * Title  
  * Meta description  
  * H1 tags  
  * Images (alt text)  
* Convert findings into structured issues  
* Design and manage database structure:  
  * Sites  
  * Pages  
  * Issues  
  * (Optional) Metrics  
* Build API endpoints:  
  * POST /crawl  
  * GET /issues  
  * GET /issues-priority  
  * GET /pages  
* Implement priority scoring logic:  
  * Severity-based scoring  
  * Optional traffic weighting

### Nice to Have

* Store crawl history  
* Deduplicate pages  
* Improve error handling and logging

### Deliverable

A backend that can scan a website, generate issues, and store structured data for frontend use.

# AI Engineer (Moe)

## AI Engineer

### Goal

Transform the platform into an intelligent assistant that not only detects issues but also recommends and simulates fixes.

### Core Responsibilities

Move from "Detection" to "Solution."

* **Structured Output:** Force the LLM to return valid JSON (Explanation \+ Fixed Code Snippet).  
* **Confidence Scoring:** Program the AI to return a "Confidence Level" so non-technical users know when to double-check a fix.  
* **Automation Simulation:** Create the logic for "Auto-fix" previews that show exactly what change will be made to the HTML.  
* Build AI recommendation engine  
  * Input: issue \+ page context  
  * Output: suggested fix (e.g., meta description, alt text)  
* Develop agent-like behavior:  
  * Explain issues in plain language  
  * Suggest improvements  
  * Generate optimized content  
* Integrate with watsonx (preferred) or another LLM

### Nice to Have

* “Auto-fix simulation”  
  * User clicks “Fix”  
  * AI generates improved version of content or HTML  
* Context-aware recommendations based on page content

### Deliverable

AI-powered suggestions that enhance the value of detected issues and demonstrate automation potential.

# Fallback Plan

# Lesser Version (Fallback Plan)

If time is limited, we will reduce scope:

### Simplifications

* Single-page crawl only  
* No multi-page tracking  
* Minimal or no database relationships

### Frontend

* Simple dashboard with issue list

### Backend

* Basic crawler returning issues (no persistence required)

### AI

* Single endpoint for generating recommendations

### Demo Flow

1. Enter URL  
2. Display issues  
3. Click issue → show AI suggestion

# TO-DO:

# TO-DO:

**The Workflow:**

1. **Frontend** sends `POST /scans { url: "example.gov" }`.  
2. **Backend** generates a `UUID` for the job, kicks off a background task (using **Celery** or **FastAPI's BackgroundTasks**), and immediately returns the ID to the frontend.  
3. **Frontend** enters a "Loading State" and polls `GET /scans/{id}` to check progress.  
4. **Backend** (Playwright) crawls, stores data, and updates the status to "Completed."

**Database Schema (SQL)**

* highly hierarchical data  
  * (Site → Page → Issue)  
* Relational database (**SQLite)**

| Table | Key Fields |
| :---- | :---- |
| **Sites** | id, domain\_url, created\_at, global\_score |
| **Pages** | id, site\_id, url, title, meta\_tags |
| **Issues** | id, page\_id, type (SEO/A11y), severity, description, snippet |
| **Recommendations** | id, issue\_id, suggested\_fix\_html, ai\_explanation |


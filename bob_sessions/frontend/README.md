# Frontend Development - Bob Sessions

## Role: Frontend Engineer (Arvin)

### Goal
Build a "Perfect 100" Lighthouse-scored dashboard that displays issues and allows users to trigger scans.

## Core Responsibilities

### 1. Hybrid Rendering
- **SSR** for scan results (dynamic data)
- **SSG** for documentation pages (static content)
- **Zero-JS** default for maximum performance
- **View Transitions API** for smooth navigation

### 2. Vue Islands
- Interactive components only where needed
- "Scan Input" form with validation
- "Real-time Progress" tracker with polling
- "AI Fix Preview" with before/after comparison
- "Issue Table" with sorting and filtering

### 3. WCAG 2.1 AA Compliance
- Semantic HTML structure
- Proper heading hierarchy
- Keyboard navigation support
- Screen reader compatibility
- Color contrast compliance
- Focus indicators

### 4. Dashboard Features
- URL input field with validation
- "Scan Website" button
- Issue table displaying:
  - Type (SEO, Accessibility, QA)
  - Severity (High, Medium, Low)
  - Priority score
  - Page URL
  - Description
- Page-level view (click page → see its issues)
- Filters for issue type and severity
- Status badges for visual clarity

## Tech Stack

- **Framework**: Astro 4.0+
- **Islands**: Vue 3 (Composition API)
- **Styling**: TailwindCSS or [getdesign.md](https://getdesign.md/)
- **Icons**: Lucide Icons or Heroicons
- **HTTP Client**: Fetch API or Axios
- **State Management**: Vue Composables (no Vuex needed)

## Development Workflow

### Setting Up
```bash
cd src/frontend
npm create astro@latest . -- --template minimal
npm install
npm install vue @astrojs/vue
npm install -D tailwindcss
```

### Running the Server
```bash
npm run dev
# Opens at http://localhost:4321
```

### Building for Production
```bash
npm run build
npm run preview
```

## Project Structure

```
src/frontend/
├── src/
│   ├── pages/
│   │   ├── index.astro           # Landing page
│   │   ├── dashboard.astro       # Main dashboard
│   │   ├── scan/[id].astro       # Scan results page
│   │   └── docs/
│   │       └── [...slug].astro   # Documentation
│   ├── components/
│   │   ├── ScanForm.vue          # Interactive scan input
│   │   ├── ProgressTracker.vue   # Real-time progress
│   │   ├── IssueTable.vue        # Issue display
│   │   ├── IssueCard.vue         # Individual issue
│   │   ├── FixPreview.vue        # Before/after comparison
│   │   └── ui/                   # Reusable UI components
│   ├── layouts/
│   │   ├── BaseLayout.astro      # Base HTML structure
│   │   └── DashboardLayout.astro # Dashboard wrapper
│   ├── lib/
│   │   ├── api.ts                # API client
│   │   ├── types.ts              # TypeScript types
│   │   └── utils.ts              # Utility functions
│   └── styles/
│       └── global.css            # Global styles
├── public/
│   └── favicon.svg
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
└── package.json
```

## API Integration

### Endpoints to Use

```typescript
// Start a scan
POST /api/v1/scans
Body: { url: string }
Response: { scan_id: string, status: string }

// Poll scan status
GET /api/v1/scans/{scan_id}
Response: { scan_id: string, status: string, progress: number, pages_scanned: number }

// Get scan results
GET /api/v1/scans/{scan_id}/results
Response: { site: {...}, pages: [...], issues: [...] }

// Get issues with filters
GET /api/v1/issues?type=seo&severity=high
Response: { issues: [...] }

// Get AI recommendation
GET /api/v1/recommendations/{issue_id}
Response: { suggested_fix_html: string, ai_explanation: string, confidence_score: number }
```

### API Client Example

```typescript
// src/lib/api.ts
const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function startScan(url: string) {
  const response = await fetch(`${API_BASE}/scans`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return response.json();
}

export async function getScanStatus(scanId: string) {
  const response = await fetch(`${API_BASE}/scans/${scanId}`);
  return response.json();
}
```

## Component Examples

### Scan Form (Vue Island)
```vue
<!-- components/ScanForm.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import { startScan } from '../lib/api';

const url = ref('');
const loading = ref(false);
const error = ref('');

async function handleSubmit() {
  loading.value = true;
  error.value = '';
  
  try {
    const result = await startScan(url.value);
    window.location.href = `/scan/${result.scan_id}`;
  } catch (e) {
    error.value = 'Failed to start scan. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="scan-form">
    <label for="url">Website URL</label>
    <input
      id="url"
      v-model="url"
      type="url"
      placeholder="https://example.gov"
      required
      :disabled="loading"
    />
    <button type="submit" :disabled="loading">
      {{ loading ? 'Scanning...' : 'Scan Website' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>
```

### Progress Tracker (Vue Island)
```vue
<!-- components/ProgressTracker.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { getScanStatus } from '../lib/api';

const props = defineProps<{ scanId: string }>();
const status = ref('pending');
const progress = ref(0);
const pagesScanned = ref(0);

let pollInterval: number;

onMounted(() => {
  pollInterval = setInterval(async () => {
    const data = await getScanStatus(props.scanId);
    status.value = data.status;
    progress.value = data.progress || 0;
    pagesScanned.value = data.pages_scanned || 0;
    
    if (data.status === 'completed' || data.status === 'failed') {
      clearInterval(pollInterval);
      if (data.status === 'completed') {
        window.location.reload();
      }
    }
  }, 2000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>

<template>
  <div class="progress-tracker">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
    </div>
    <p>{{ status }} - {{ pagesScanned }} pages scanned</p>
  </div>
</template>
```

## Astro Page Example

```astro
---
// src/pages/dashboard.astro
import BaseLayout from '../layouts/BaseLayout.astro';
import ScanForm from '../components/ScanForm.vue';

const title = 'Dashboard - PublicPulse AI';
---

<BaseLayout title={title}>
  <main>
    <h1>Website Audit Dashboard</h1>
    <p>Enter a website URL to start scanning for SEO and accessibility issues.</p>
    
    <!-- Vue Island - only this component is interactive -->
    <ScanForm client:load />
    
    <!-- Static content - zero JS -->
    <section>
      <h2>What We Check</h2>
      <ul>
        <li>SEO: Meta tags, headings, content structure</li>
        <li>Accessibility: WCAG 2.1 AA compliance</li>
        <li>Performance: Page load metrics</li>
      </ul>
    </section>
  </main>
</BaseLayout>
```

## Accessibility Checklist

- [ ] All images have alt text
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators are visible
- [ ] Form labels are properly associated
- [ ] ARIA labels where needed
- [ ] Skip to main content link
- [ ] Screen reader tested

## Performance Targets

- **Lighthouse Performance**: 100/100
- **Lighthouse Accessibility**: 100/100
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Total Bundle Size**: < 100KB (excluding images)

## Nice to Have Features

- Dark mode toggle
- Export issues to CSV
- Print-friendly view
- Keyboard shortcuts
- Issue history comparison
- Shareable scan links

## Integration Points

### With Backend (Shawn)
- Confirm API response formats
- Handle loading and error states
- Implement polling for scan progress
- Display all issue types correctly

### With AI Engineer (Moe)
- Display AI recommendations
- Show confidence scores
- Render before/after HTML previews
- Handle recommendation errors

### With Product Lead (Frank)
- Validate user flow
- Ensure demo scenarios work
- Test with realistic data
- Gather feedback on UX

## Session Documentation

Document your Bob sessions:
- `session_001_astro_setup.md` - Initial Astro configuration
- `session_002_dashboard_ui.md` - Dashboard implementation
- `session_003_vue_islands.md` - Interactive components
- `session_004_api_integration.md` - Backend integration
- etc.

## Resources

- [Astro Documentation](https://docs.astro.build/)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
- [getdesign.md](https://getdesign.md/) - Design system

## Success Metrics

- [ ] Dashboard loads in < 2 seconds
- [ ] Lighthouse score 100/100 (Performance & A11y)
- [ ] Can scan a website successfully
- [ ] Issues display correctly
- [ ] Filters work as expected
- [ ] Mobile responsive
- [ ] Works on older browsers
- [ ] Screen reader compatible

---

**Remember**: The dashboard itself should be a showcase of accessibility and performance. Practice what we preach!
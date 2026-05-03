# PublicPulse AI - Frontend

High-performance Astro-based dashboard with Vue Islands for the PublicPulse AI platform.

## 🚀 Tech Stack

- **Astro 4.15+**: Static site generator with Islands Architecture
- **Vue 3.5+**: Interactive components (Composition API)
- **TypeScript**: Type safety
- **TailwindCSS 3.4+**: Utility-first styling
- **Fetch API**: HTTP requests to backend

## 📁 Project Structure

```
src/frontend/
├── src/
│   ├── pages/
│   │   ├── index.astro           # Landing page
│   │   └── dashboard.astro       # Main dashboard
│   ├── components/
│   │   └── ScanForm.vue          # Interactive scan input
│   ├── layouts/
│   │   └── BaseLayout.astro      # Base HTML structure
│   ├── lib/
│   │   ├── api.ts                # API client with polling
│   │   └── types.ts              # TypeScript types
│   ├── styles/
│   │   └── global.css            # Global styles
│   └── env.d.ts                  # Environment types
├── public/
│   └── favicon.svg
├── astro.config.mjs              # Astro configuration
├── tailwind.config.mjs           # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json
```

## 🛠️ Setup

### Prerequisites

- Node.js 18+ 
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 Development

The development server runs at `http://localhost:4321`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production (includes type checking)
- `npm run preview` - Preview production build
- `npm run check` - Run Astro type checking

## 🏗️ Architecture

### Islands Architecture

This project uses Astro's Islands Architecture:

- **Static HTML (Zero-JS)**: Most of the site is static HTML with no JavaScript
- **Vue Islands**: Interactive components are hydrated only where needed
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

### Key Features

- ⚡ **Zero-JS by Default**: Maximum performance
- 🏝️ **Vue Islands**: Interactive components only where needed
- ♿ **WCAG 2.1 AA Compliant**: Accessibility first
- 📱 **Responsive**: Mobile-first design
- 🎨 **TailwindCSS**: Utility-first styling

## 🔌 API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api/v1`

### Environment Variables

Create a `.env` file (optional):

```env
PUBLIC_API_URL=http://localhost:8000/api/v1
```

### API Client

The `src/lib/api.ts` file provides:

- `startScan(url)` - Start a new website scan
- `getScanStatus(scanId)` - Get scan status
- `pollScanStatus(scanId, onProgress)` - Poll until completion
- `getScanResults(scanId)` - Get scan results
- `getIssues(filters)` - Get issues with filters
- `getRecommendation(issueId)` - Get AI recommendations

## 📝 Component Development

### Creating a Vue Island

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
  <button @click="count++">
    Count: {{ count }}
  </button>
</template>
```

### Using in Astro Page

```astro
---
import MyComponent from '../components/MyComponent.vue';
---

<MyComponent client:load />
```

### Client Directives

- `client:load` - Load immediately
- `client:visible` - Load when visible
- `client:idle` - Load when browser is idle
- `client:only="vue"` - Only render on client

## ♿ Accessibility

This project follows WCAG 2.1 AA standards:

- ✅ Semantic HTML
- ✅ Proper heading hierarchy
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast compliance
- ✅ Focus indicators
- ✅ ARIA labels where needed

## 🎯 Performance Targets

- **Lighthouse Performance**: 100/100
- **Lighthouse Accessibility**: 100/100
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Total Bundle Size**: < 100KB (excluding images)

## 🧪 Testing

```bash
# Type checking
npm run check

# Build test
npm run build
```

## 📚 Resources

- [Astro Documentation](https://docs.astro.build/)
- [Vue 3 Documentation](https://vuejs.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## 🤝 Contributing

1. Follow the existing code style
2. Ensure accessibility compliance
3. Test on multiple browsers
4. Keep bundle size minimal
5. Document new components

## 📄 License

MIT License - see root LICENSE file for details

---

**Built with ❤️ for public service organizations**
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Brand & Accent Colors (MongoDB-inspired)
        'brand-green': '#00ED64',
        'brand-green-dark': '#00684A',
        'brand-green-mid': '#00B050',
        'brand-green-soft': '#E3FCF0',
        'brand-teal-deep': '#001E2B',
        'brand-teal': '#00495C',
        'brand-teal-mid': '#003545',
        
        // Category Accent Colors (Course Tags)
        'accent-purple': '#7B61FF',
        'accent-orange': '#FF6B35',
        'accent-pink': '#FF4D8D',
        'accent-blue': '#0091FF',
        
        // Surface Colors
        'canvas': '#FFFFFF',
        'canvas-dark': '#13131A',
        'surface': '#F9FAFB',
        'surface-soft': '#F3F4F6',
        'surface-feature': '#E3FCF0',
        
        // Border Colors
        'hairline': '#E5E7EB',
        'hairline-soft': '#F3F4F6',
        'hairline-strong': '#D1D5DB',
        'hairline-dark': '#374151',
        
        // Text Colors
        'ink': '#001E2B',
        'charcoal': '#1F2937',
        'slate': '#5C6C75',
        'steel': '#89979B',
        'stone': '#9CA3AF',
        'muted': '#D1D5DB',
        'on-dark': '#FFFFFF',
        'on-dark-muted': 'rgba(255, 255, 255, 0.7)',
        'on-primary': '#001E2B',
        
        // Semantic Colors
        'semantic-warning-bg': '#FEF3C7',
        'semantic-warning-text': '#92400E',
        'semantic-error-bg': '#FEE2E2',
        'semantic-error-text': '#991B1B',
        'semantic-success-bg': '#D1FAE5',
        'semantic-success-text': '#065F46',
        
        // Interactive States
        'primary-pressed': '#00B050',
      },
      fontFamily: {
        sans: ['Euclid Circular A', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['Source Code Pro', 'SF Mono', 'Menlo', 'Consolas', 'monospace'],
      },
      fontSize: {
        // Typography Hierarchy
        'hero-display': ['72px', { lineHeight: '1.10', letterSpacing: '-1.5px', fontWeight: '500' }],
        'display-lg': ['56px', { lineHeight: '1.15', letterSpacing: '-1px', fontWeight: '500' }],
        'heading-1': ['48px', { lineHeight: '1.20', letterSpacing: '-0.5px', fontWeight: '500' }],
        'heading-2': ['36px', { lineHeight: '1.25', letterSpacing: '-0.5px', fontWeight: '500' }],
        'heading-3': ['28px', { lineHeight: '1.30', letterSpacing: '0', fontWeight: '500' }],
        'heading-4': ['22px', { lineHeight: '1.35', letterSpacing: '0', fontWeight: '500' }],
        'heading-5': ['18px', { lineHeight: '1.40', letterSpacing: '0', fontWeight: '600' }],
        'subtitle': ['18px', { lineHeight: '1.50', letterSpacing: '0', fontWeight: '400' }],
        'body-md': ['16px', { lineHeight: '1.55', letterSpacing: '0', fontWeight: '400' }],
        'body-sm': ['14px', { lineHeight: '1.50', letterSpacing: '0', fontWeight: '400' }],
        'body-sm-medium': ['14px', { lineHeight: '1.50', letterSpacing: '0', fontWeight: '500' }],
        'caption-bold': ['13px', { lineHeight: '1.40', letterSpacing: '0', fontWeight: '600' }],
        'micro-uppercase': ['11px', { lineHeight: '1.40', letterSpacing: '1px', fontWeight: '600' }],
        'button-md': ['14px', { lineHeight: '1.30', letterSpacing: '0', fontWeight: '600' }],
        'code-md': ['14px', { lineHeight: '1.55', letterSpacing: '0', fontWeight: '400' }],
      },
      spacing: {
        // Enhanced Spacing System (4px base unit)
        '3xs': '2px',
        '2xs': '4px',
        'xxs': '4px',
        'xs': '8px',
        'sm': '12px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '40px',
        'xxl': '48px',
        '3xl': '48px',
        '4xl': '64px',
        'section': '64px',
        '5xl': '80px',
        '6xl': '96px',
        'section-lg': '96px',
        '7xl': '120px',
        'hero': '120px',
      },
      borderRadius: {
        // Border Radius Scale
        'xs': '4px',
        'sm': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'xxl': '24px',
        'full': '9999px',
      },
      boxShadow: {
        // Elevation System
        'subtle': 'rgba(0, 30, 43, 0.04) 0px 1px 2px 0px',
        'card': 'rgba(0, 30, 43, 0.08) 0px 4px 12px 0px',
        'mockup': 'rgba(0, 30, 43, 0.12) 0px 12px 24px -4px',
        'modal': 'rgba(0, 30, 43, 0.16) 0px 16px 48px -8px',
      },
      screens: {
        // Responsive Breakpoints
        'mobile-sm': '480px',
        'mobile-lg': '767px',
        'tablet': '768px',
        'desktop': '1024px',
        'wide': '1280px',
      },
    },
  },
  plugins: [],
};

// Made with Bob - MongoDB Design System Implementation

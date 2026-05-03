<script setup lang="ts">
import { ref } from 'vue';
import { startScan } from '../lib/api';

const url = ref('');
const loading = ref(false);
const error = ref('');
const success = ref('');
const statusMessage = ref('');

async function handleSubmit() {
  // Reset states
  loading.value = true;
  error.value = '';
  success.value = '';
  statusMessage.value = 'Starting scan...';
  
  try {
    const result = await startScan(url.value);
    success.value = 'Scan started successfully! Redirecting to results...';
    statusMessage.value = 'Scan started successfully';
    
    // Redirect to scan results page after a short delay
    setTimeout(() => {
      window.location.href = `/scan/${result.scan_id}`;
    }, 1500);
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to start scan. Please try again.';
    statusMessage.value = 'Scan failed';
  } finally {
    loading.value = false;
  }
}

function validateUrl(): boolean {
  if (!url.value) {
    error.value = 'Please enter a URL';
    return false;
  }
  
  if (!url.value.startsWith('http://') && !url.value.startsWith('https://')) {
    error.value = 'URL must start with http:// or https://';
    return false;
  }
  
  return true;
}

function handleFormSubmit(e: Event) {
  e.preventDefault();
  error.value = '';
  
  if (validateUrl()) {
    handleSubmit();
  }
}
</script>

<template>
  <div class="space-y-8">
    <!-- Form Header -->
    <div class="text-center">
      <h2 class="text-heading-3 text-ink mb-3">Scan Your Website</h2>
      <p class="text-lg text-slate max-w-2xl mx-auto">
        Enter your website URL to start a comprehensive SEO and accessibility audit.
      </p>
    </div>
    
    <!-- Form -->
    <form @submit="handleFormSubmit" class="space-y-6" novalidate>
      <!-- URL Input -->
      <div>
        <label
          for="url"
          class="block text-body-md font-semibold text-ink mb-3"
        >
          Website URL
          <span class="text-semantic-error-text" aria-label="required">*</span>
        </label>
        <input
          id="url"
          v-model="url"
          type="url"
          placeholder="https://example.gov"
          required
          :disabled="loading"
          class="input w-full h-14 text-lg"
          aria-describedby="url-help"
          aria-required="true"
          aria-invalid="error ? 'true' : 'false'"
          :aria-errormessage="error ? 'url-error' : undefined"
        />
        <p id="url-help" class="text-body-sm text-slate mt-2">
          Enter the full URL including http:// or https://
        </p>
      </div>

      <!-- Error Alert -->
      <div
        v-if="error"
        id="url-error"
        role="alert"
        class="alert-error"
      >
        <div class="flex items-start gap-2">
          <svg
            class="w-5 h-5 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <div>
            <p class="font-semibold">Error</p>
            <p>{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Success Alert -->
      <div
        v-if="success"
        role="status"
        class="alert-success"
      >
        <div class="flex items-start gap-2">
          <svg
            class="w-5 h-5 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <div>
            <p class="font-semibold">Success</p>
            <p>{{ success }}</p>
          </div>
        </div>
      </div>

      <!-- Submit Button - Enhanced MongoDB Pill Style -->
      <button
        type="submit"
        :disabled="loading"
        class="btn-primary w-full h-14 text-lg"
        :aria-busy="loading ? 'true' : 'false'"
      >
        <span v-if="loading" class="flex items-center justify-center gap-3">
          <svg
            class="spinner"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
              fill="none"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Scanning...
        </span>
        <span v-else>Scan Website</span>
      </button>
    </form>

    <!-- Live Region for Screen Readers -->
    <div
      aria-live="polite"
      aria-atomic="true"
      class="sr-only"
    >
      {{ statusMessage }}
    </div>

    <!-- Info Section - Enhanced spacing -->
    <div class="pt-8 border-t border-hairline">
      <h3 class="text-body-md font-semibold text-ink mb-4">What we check:</h3>
      <ul class="space-y-4" role="list">
        <li class="flex items-start gap-2 text-body-sm text-slate">
          <svg
            class="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <span><strong>SEO:</strong> Meta tags, headings, content structure</span>
        </li>
        <li class="flex items-start gap-2 text-body-sm text-slate">
          <svg
            class="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <span><strong>Accessibility:</strong> WCAG 2.1 AA compliance</span>
        </li>
        <li class="flex items-start gap-2 text-body-sm text-slate">
          <svg
            class="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <span><strong>Performance:</strong> Page load metrics</span>
        </li>
        <li class="flex items-start gap-2 text-body-sm text-slate">
          <svg
            class="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <span><strong>Quality:</strong> Best practices and common issues</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/* Spinner animation */
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
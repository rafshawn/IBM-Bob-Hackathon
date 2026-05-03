<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { getScanStatus, getScanResults, getRecommendation } from '../lib/api';
import type { Scan, ScanResults, Recommendation } from '../lib/types';

const props = defineProps<{
  scanId: string;
}>();

// State
const loading = ref(true);
const error = ref('');
const scan = ref<Scan | null>(null);
const results = ref<ScanResults | null>(null);
const pollInterval = ref<number | null>(null);
const selectedIssueId = ref<string | null>(null);
const recommendation = ref<Recommendation | null>(null);
const loadingRecommendation = ref(false);
const recommendationError = ref('');

// Fetch scan status
async function fetchScanStatus() {
  try {
    const data = await getScanStatus(props.scanId);
    scan.value = data;

    // If completed, fetch full results
    if (data.status === 'completed') {
      await fetchResults();
      stopPolling();
    } else if (data.status === 'failed') {
      error.value = data.error_message || 'Scan failed. Please try again.';
      stopPolling();
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to fetch scan status';
    stopPolling();
  } finally {
    loading.value = false;
  }
}

// Fetch complete results
async function fetchResults() {
  try {
    const data = await getScanResults(props.scanId);
    results.value = data;
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to fetch scan results';
  }
}

// Start polling
function startPolling() {
  pollInterval.value = window.setInterval(() => {
    fetchScanStatus();
  }, 2000); // Poll every 2 seconds
}

// Stop polling
function stopPolling() {
  if (pollInterval.value) {
    clearInterval(pollInterval.value);
    pollInterval.value = null;
  }
}

// Lifecycle
onMounted(() => {
  fetchScanStatus();
  startPolling();
});

onUnmounted(() => {
  stopPolling();
});

// Helper functions
function getSeverityColor(severity: string): string {
  switch (severity) {
    case 'high':
      return 'bg-red-100 text-red-800 border-red-200';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case 'low':
      return 'bg-blue-100 text-blue-800 border-blue-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

function getTypeColor(type: string): string {
  switch (type) {
    case 'accessibility':
      return 'bg-purple-100 text-purple-800 border-purple-200';
    case 'seo':
      return 'bg-green-100 text-green-800 border-green-200';
    case 'qa':
      return 'bg-orange-100 text-orange-800 border-orange-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}

function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleString();
}

// Fetch recommendation for an issue
async function fetchRecommendation(issueId: string) {
  if (selectedIssueId.value === issueId && recommendation.value) {
    // Toggle off if clicking the same issue
    selectedIssueId.value = null;
    recommendation.value = null;
    return;
  }

  selectedIssueId.value = issueId;
  loadingRecommendation.value = true;
  recommendationError.value = '';
  recommendation.value = null;

  try {
    const data = await getRecommendation(issueId);
    recommendation.value = data;
  } catch (e) {
    recommendationError.value = e instanceof Error ? e.message : 'Failed to fetch recommendation';
  } finally {
    loadingRecommendation.value = false;
  }
}
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-brand-green"></div>
      <p class="mt-4 text-slate">Loading scan data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert-error">
      <div class="flex items-start gap-2">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <div>
          <p class="font-semibold">Error</p>
          <p>{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Scanning in Progress -->
    <div v-else-if="scan && (scan.status === 'pending' || scan.status === 'in_progress')" class="space-y-6">
      <div class="card-content">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-heading-4 text-ink">Scanning in Progress</h2>
          <span class="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
            {{ scan.status === 'pending' ? 'Starting...' : 'In Progress' }}
          </span>
        </div>

        <!-- Progress Bar -->
        <div class="mb-6">
          <div class="flex justify-between text-sm text-slate mb-2">
            <span>Progress</span>
            <span>{{ scan.progress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              class="bg-brand-green h-3 rounded-full transition-all duration-500"
              :style="{ width: `${scan.progress}%` }"
            ></div>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-2 gap-4">
          <div class="text-center p-4 bg-surface rounded-lg">
            <p class="text-2xl font-bold text-ink">{{ scan.pages_scanned }}</p>
            <p class="text-sm text-slate">Pages Scanned</p>
          </div>
          <div class="text-center p-4 bg-surface rounded-lg">
            <p class="text-2xl font-bold text-ink">{{ scan.total_pages || '...' }}</p>
            <p class="text-sm text-slate">Total Pages</p>
          </div>
        </div>

        <p class="text-sm text-slate mt-4 text-center">
          This may take a few minutes. You can leave this page and come back later.
        </p>
      </div>
    </div>

    <!-- Results Display -->
    <div v-else-if="scan && scan.status === 'completed' && results" class="space-y-6">
      <!-- Summary Cards -->
      <div class="grid md:grid-cols-4 gap-4">
        <!-- Global Score -->
        <div class="card-content text-center">
          <p class="text-sm text-slate mb-2">Quality Score</p>
          <p class="text-4xl font-bold" :class="getScoreColor(results.global_score || 0)">
            {{ results.global_score?.toFixed(1) || 'N/A' }}
          </p>
          <p class="text-xs text-slate mt-1">out of 100</p>
        </div>

        <!-- Pages Scanned -->
        <div class="card-content text-center">
          <p class="text-sm text-slate mb-2">Pages Scanned</p>
          <p class="text-4xl font-bold text-ink">{{ results.pages_scanned }}</p>
        </div>

        <!-- Total Issues -->
        <div class="card-content text-center">
          <p class="text-sm text-slate mb-2">Total Issues</p>
          <p class="text-4xl font-bold text-ink">{{ results.total_issues }}</p>
        </div>

        <!-- Scan Date -->
        <div class="card-content text-center">
          <p class="text-sm text-slate mb-2">Scanned</p>
          <p class="text-sm font-medium text-ink">{{ formatDate(results.created_at) }}</p>
        </div>
      </div>

      <!-- Issues by Type -->
      <div class="card-content">
        <h3 class="text-heading-4 text-ink mb-4">Issues by Type</h3>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="flex items-center justify-between p-4 bg-surface rounded-lg">
            <div>
              <p class="text-sm text-slate">Accessibility</p>
              <p class="text-2xl font-bold text-ink">{{ results.issues_by_type.accessibility || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>

          <div class="flex items-center justify-between p-4 bg-surface rounded-lg">
            <div>
              <p class="text-sm text-slate">SEO</p>
              <p class="text-2xl font-bold text-ink">{{ results.issues_by_type.seo || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <div class="flex items-center justify-between p-4 bg-surface rounded-lg">
            <div>
              <p class="text-sm text-slate">Quality Assurance</p>
              <p class="text-2xl font-bold text-ink">{{ results.issues_by_type.qa || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Issues by Severity -->
      <div class="card-content">
        <h3 class="text-heading-4 text-ink mb-4">Issues by Severity</h3>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-800 font-medium">High Priority</p>
            <p class="text-3xl font-bold text-red-600">{{ results.issues_by_severity.high || 0 }}</p>
          </div>
          <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p class="text-sm text-yellow-800 font-medium">Medium Priority</p>
            <p class="text-3xl font-bold text-yellow-600">{{ results.issues_by_severity.medium || 0 }}</p>
          </div>
          <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p class="text-sm text-blue-800 font-medium">Low Priority</p>
            <p class="text-3xl font-bold text-blue-600">{{ results.issues_by_severity.low || 0 }}</p>
          </div>
        </div>
      </div>

      <!-- Top Issues -->
      <div class="card-content">
        <h3 class="text-heading-4 text-ink mb-4">Top Priority Issues</h3>
        <div v-if="results.top_issues.length === 0" class="text-center py-8 text-slate">
          <p>No issues detected! Your website looks great! 🎉</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="issue in results.top_issues"
            :key="issue.id"
            class="border border-hairline rounded-lg p-4 hover:border-brand-green transition-colors"
            :class="{ 'border-brand-green border-2': selectedIssueId === issue.id }"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <span class="px-2 py-1 rounded text-xs font-medium border" :class="getTypeColor(issue.type)">
                    {{ issue.type.toUpperCase() }}
                  </span>
                  <span class="px-2 py-1 rounded text-xs font-medium border" :class="getSeverityColor(issue.severity)">
                    {{ issue.severity.toUpperCase() }}
                  </span>
                  <span class="text-xs text-slate">Priority: {{ issue.priority_score }}</span>
                </div>
                <h4 class="text-lg font-semibold text-ink mb-1">{{ issue.title }}</h4>
                <p class="text-sm text-slate mb-2">{{ issue.description }}</p>
                <p v-if="issue.page_url" class="text-xs text-slate">
                  Page: <code class="bg-surface px-1 py-0.5 rounded">{{ issue.page_url }}</code>
                </p>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="mt-3 flex gap-2">
              <button
                @click="fetchRecommendation(issue.id)"
                class="btn-secondary text-sm"
                :disabled="loadingRecommendation && selectedIssueId === issue.id"
              >
                <span v-if="loadingRecommendation && selectedIssueId === issue.id">Loading...</span>
                <span v-else-if="selectedIssueId === issue.id">Hide AI Fix</span>
                <span v-else>Get AI Fix</span>
              </button>
              <details v-if="issue.snippet" class="inline-block">
                <summary class="cursor-pointer text-sm text-brand-green hover:text-brand-green-dark px-3 py-1">
                  View Code Snippet
                </summary>
                <pre class="mt-2 p-3 bg-surface rounded text-xs overflow-x-auto"><code>{{ issue.snippet }}</code></pre>
              </details>
            </div>

            <!-- Recommendation Display -->
            <div v-if="selectedIssueId === issue.id && recommendation" class="mt-4 border-t border-hairline pt-4">
              <h5 class="text-md font-semibold text-ink mb-3 flex items-center gap-2">
                <svg class="w-5 h-5 text-brand-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                AI-Powered Fix Recommendation
              </h5>
              
              <!-- Explanation -->
              <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p class="text-sm text-ink leading-relaxed">{{ recommendation.explanation }}</p>
              </div>

              <!-- Before/After Code -->
              <div class="grid md:grid-cols-2 gap-4 mb-4">
                <!-- Before -->
                <div>
                  <h6 class="text-sm font-semibold text-red-700 mb-2 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Before (Current Code)
                  </h6>
                  <pre class="p-3 bg-red-50 border border-red-200 rounded text-xs overflow-x-auto"><code>{{ recommendation.before_snippet }}</code></pre>
                </div>
                
                <!-- After -->
                <div>
                  <h6 class="text-sm font-semibold text-green-700 mb-2 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    After (Recommended Fix)
                  </h6>
                  <pre class="p-3 bg-green-50 border border-green-200 rounded text-xs overflow-x-auto"><code>{{ recommendation.after_snippet }}</code></pre>
                </div>
              </div>

              <!-- Metadata -->
              <div class="flex items-center gap-4 text-xs text-slate">
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Confidence: {{ (recommendation.confidence_score * 100).toFixed(0) }}%
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Model: {{ recommendation.model_used }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Status: {{ recommendation.status }}
                </span>
              </div>
            </div>

            <!-- Recommendation Error -->
            <div v-if="selectedIssueId === issue.id && recommendationError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-800">{{ recommendationError }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Scanned Pages -->
      <div class="card-content">
        <h3 class="text-heading-4 text-ink mb-4">Scanned Pages ({{ results.pages.length }})</h3>
        <div class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="page in results.pages"
            :key="page.id"
            class="p-3 bg-surface rounded-lg hover:bg-gray-50 transition-colors"
          >
            <p class="font-medium text-ink text-sm">{{ page.title || 'Untitled Page' }}</p>
            <p class="text-xs text-slate truncate">{{ page.url }}</p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-4 justify-center">
        <a href="/dashboard" class="btn-secondary">
          Start New Scan
        </a>
        <button
          @click="window.print()"
          class="btn-secondary"
        >
          Print Report
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media print {
  button {
    display: none;
  }
}
</style>
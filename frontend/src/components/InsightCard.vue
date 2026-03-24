<template>
  <div class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md hover:shadow-gray-100 transition-all">

    <!-- Header -->
    <div class="flex items-start justify-between mb-4 gap-3">
      <div class="flex-1 min-w-0">
        <h3 class="text-sm font-bold text-gray-900 leading-snug">{{ insight.title }}</h3>
        <p class="text-xs text-gray-400 mt-1">
          {{ new Date(insight.generated_at).toLocaleDateString('en-US', {
            day:'numeric', month:'short', year:'numeric',
            hour:'2-digit', minute:'2-digit'
          }) }}
        </p>
      </div>
      <div class="flex items-center gap-2 flex-shrink-0">
        <span class="px-2.5 py-1 rounded-lg text-xs font-semibold"
          :class="{
            'bg-blue-50 text-blue-700':   insight.category === 'Sales',
            'bg-green-50 text-green-700': insight.category === 'Marketing',
            'bg-amber-50 text-amber-700': insight.category === 'Support'
          }">
          {{ insight.category }}
        </span>
        <button @click="exportPDF" :disabled="exporting"
          class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-gray-200 text-xs font-semibold text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 transition-all disabled:opacity-50">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          {{ exporting ? '...' : 'PDF' }}
        </button>
      </div>
    </div>

    <!-- Divider -->
    <div class="h-px bg-gray-50 mb-4"/>

    <!-- Content -->
    <div class="text-sm text-gray-600 leading-relaxed whitespace-pre-line">
      {{ insight.content }}
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { exportInsightToPDF } from '../services/pdfExport'

const props    = defineProps({ insight: Object })
const exporting = ref(false)

async function exportPDF() {
  exporting.value = true
  try { exportInsightToPDF(props.insight) }
  finally { exporting.value = false }
}
</script>
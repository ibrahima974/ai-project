<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6">
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1 mr-4">
        <h3 class="text-base font-semibold text-gray-900">{{ insight.title }}</h3>
        <p class="text-xs text-gray-400 mt-0.5">
          {{ new Date(insight.generated_at).toLocaleDateString('fr-FR', {
            day: 'numeric', month: 'long', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
          }) }}
        </p>
      </div>

      <div class="flex items-center gap-2 flex-shrink-0">
        <span
          class="px-2 py-1 rounded-full text-xs font-medium"
          :class="{
            'bg-blue-50 text-blue-700':   insight.category === 'Sales',
            'bg-green-50 text-green-700': insight.category === 'Marketing',
            'bg-amber-50 text-amber-700': insight.category === 'Support'
          }"
        >
          {{ insight.category }}
        </span>

        <!-- Bouton Export PDF -->
        <button
          @click="exportPDF"
          :disabled="exporting"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-200 text-xs font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 transition-colors disabled:opacity-50"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          {{ exporting ? 'Export...' : 'PDF' }}
        </button>
      </div>
    </div>

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
  try {
    exportInsightToPDF(props.insight)
  } finally {
    exporting.value = false
  }
}
</script>
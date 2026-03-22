<template>
  <div>
    <div class="flex items-start justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Insights IA</h2>
        <p class="text-gray-400 text-sm mt-0.5">Analyses générées par Claude</p>
      </div>
    </div>

    <!-- Générateur -->
    <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
      <h3 class="text-base font-semibold text-gray-900 mb-1">
        Générer une analyse
      </h3>
      <p class="text-sm text-gray-400 mb-4">
        Claude va analyser tes métriques et générer un rapport actionnable.
      </p>

      <div class="flex gap-3">
        <select
          v-model="selectedCategory"
          class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
        >
          <option value="Sales">Sales</option>
          <option value="Marketing">Marketing</option>
          <option value="Support">Support</option>
        </select>

        <button
          @click="generate"
          :disabled="store.loading"
          class="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          <svg v-if="!store.loading" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
          </svg>
          <div v-else class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          {{ store.loading ? 'Analyse en cours...' : 'Analyser avec Claude' }}
        </button>
      </div>

      <!-- Erreur génération -->
      <div v-if="store.error" class="mt-4 bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 text-sm">
        {{ store.error }}
      </div>

      <!-- Succès -->
      <div v-if="successMsg" class="mt-4 bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 text-sm">
        {{ successMsg }}
      </div>
    </div>

    <!-- Filtre historique -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-base font-semibold text-gray-900">Historique des analyses</h3>
      <div class="flex gap-2">
        <button
          v-for="cat in ['Toutes', 'Sales', 'Marketing', 'Support']"
          :key="cat"
          @click="filterCategory = cat"
          class="px-3 py-1 rounded-full text-xs font-medium border transition-colors"
          :class="filterCategory === cat
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300'"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Loading historique -->
    <div v-if="loadingHistory" class="flex items-center justify-center h-32">
      <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Vide -->
    <div
      v-else-if="filteredInsights.length === 0"
      class="bg-white rounded-xl border border-gray-200 p-12 text-center"
    >
      <p class="text-gray-400 text-sm">Aucune analyse générée pour l'instant.</p>
      <p class="text-gray-300 text-xs mt-1">Lance ta première analyse ci-dessus.</p>
    </div>

    <!-- Liste insights -->
    <div v-else class="space-y-4">
      <InsightCard
        v-for="insight in filteredInsights"
        :key="insight.id"
        :insight="insight"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInsightsStore } from '../stores/insightsStore'
import InsightCard from '../components/InsightCard.vue'

const store            = useInsightsStore()
const selectedCategory = ref('Sales')
const filterCategory   = ref('Toutes')
const successMsg       = ref('')
const loadingHistory   = ref(false)

onMounted(async () => {
  loadingHistory.value = true
  await store.fetchInsights()
  loadingHistory.value = false
})

const filteredInsights = computed(() =>
  filterCategory.value === 'Toutes'
    ? store.insights
    : store.insights.filter(i => i.category === filterCategory.value)
)

async function generate() {
  try {
    await store.generateInsight(selectedCategory.value)
    successMsg.value = 'Analyse générée et sauvegardée avec succès.'
    setTimeout(() => successMsg.value = '', 4000)
  } catch {
    // erreur déjà gérée dans le store
  }
}
</script>
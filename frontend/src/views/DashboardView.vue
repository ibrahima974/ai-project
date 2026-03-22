<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">Dashboard</h2>
    <p class="text-gray-400 text-sm mb-8">Vue d'ensemble de tes KPIs business</p>

    <!-- Loading -->
    <div v-if="store.loading" class="flex items-center justify-center h-40">
      <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Erreur -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-200 text-red-600 rounded-lg p-4 mb-6">
      {{ store.error }}
    </div>

    <div v-else>
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <KpiCard
          label="Revenu mensuel"
          :value="latestRevenue"
          unit="€"
          :trend="2.4"
        />
        <KpiCard
          label="Nouveaux clients"
          :value="latestClients"
          unit="clients"
          :trend="8.1"
        />
        <KpiCard
          label="Taux de churn"
          :value="latestChurn"
          unit="%"
          :trend="-0.3"
        />
      </div>

      <!-- Filtre catégorie -->
      <div class="flex gap-2 mb-4">
        <button
          v-for="cat in categories"
          :key="cat"
          @click="selectedCategory = cat"
          class="px-4 py-1.5 rounded-full text-sm font-medium border transition-colors"
          :class="selectedCategory === cat
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300'"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Graphique -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h3 class="text-base font-semibold text-gray-800 mb-4">
          Évolution — {{ selectedCategory }}
        </h3>
        <apexchart
          type="line"
          height="280"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMetricsStore } from '../stores/metricsStore'
import KpiCard from '../components/KpiCard.vue'

const store            = useMetricsStore()
const categories       = ['Sales', 'Marketing', 'Support']
const selectedCategory = ref('Sales')

onMounted(() => store.fetchMetrics())

const filtered = computed(() =>
  store.metrics.filter(m => m.category === selectedCategory.value)
)

const latestRevenue = computed(() => {
  const m = store.metrics.filter(m => m.name === 'Revenu mensuel')
  return m.length ? m[0].value.toLocaleString() : '—'
})

const latestClients = computed(() => {
  const m = store.metrics.filter(m => m.name === 'Nouveaux clients')
  return m.length ? m[0].value : '—'
})

const latestChurn = computed(() => {
  const m = store.metrics.filter(m => m.name === 'Taux de churn')
  return m.length ? m[0].value : '—'
})

const uniqueNames = computed(() =>
  [...new Set(filtered.value.map(m => m.name))]
)

const chartSeries = computed(() =>
  uniqueNames.value.map(name => ({
    name,
    data: filtered.value
      .filter(m => m.name === name)
      .sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
      .map(m => m.value)
  }))
)

const chartLabels = computed(() =>
  [...new Set(
    filtered.value
      .sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
      .map(m => m.recorded_at)
  )]
)

const chartOptions = computed(() => ({
  chart:  { toolbar: { show: false }, zoom: { enabled: false } },
  stroke: { curve: 'smooth', width: 2 },
  xaxis:  { categories: chartLabels.value },
  colors: ['#3B82F6', '#10B981', '#F59E0B'],
  grid:   { borderColor: '#F3F4F6' },
  legend: { position: 'top' },
  tooltip: { y: { formatter: val => val.toLocaleString() } }
}))
</script>
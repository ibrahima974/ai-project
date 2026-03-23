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
        <KpiCard label="Revenu mensuel"   :value="latestRevenue" unit="€"       :trend="2.4"  />
        <KpiCard label="Nouveaux clients" :value="latestClients" unit="clients" :trend="8.1"  />
        <KpiCard label="Taux de churn"    :value="latestChurn"   unit="%"       :trend="-0.3" />
      </div>

      <!-- Filtres -->
      <div class="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex flex-wrap items-center gap-4">

        <!-- Filtre catégorie -->
        <div class="flex gap-2">
          <button
            v-for="cat in categories" :key="cat"
            @click="selectedCategory = cat"
            class="px-4 py-1.5 rounded-full text-sm font-medium border transition-colors"
            :class="selectedCategory === cat
              ? 'bg-blue-600 text-white border-blue-600'
              : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300'"
          >
            {{ cat }}
          </button>
        </div>

        <div class="h-6 w-px bg-gray-200"></div>

        <!-- Date range picker -->
        <div class="flex items-center gap-2 text-sm">
          <label class="text-gray-500">Du</label>
          <input
            v-model="dateFrom" type="date"
            class="border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-blue-400"
          />
          <label class="text-gray-500">au</label>
          <input
            v-model="dateTo" type="date"
            class="border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-blue-400"
          />
          <button
            @click="resetDates"
            class="text-xs text-gray-400 hover:text-gray-600 underline"
          >
            Réinitialiser
          </button>
        </div>

        <!-- Sélecteur de graphique -->
        <div class="ml-auto flex gap-2">
          <button
            v-for="type in chartTypes" :key="type.value"
            @click="selectedChart = type.value"
            class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors"
            :class="selectedChart === type.value
              ? 'bg-gray-900 text-white border-gray-900'
              : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400'"
          >
            {{ type.label }}
          </button>
        </div>
      </div>

      <!-- Graphiques -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h3 class="text-base font-semibold text-gray-800 mb-1">
          {{ chartTitle }}
        </h3>
        <p class="text-xs text-gray-400 mb-4">
          {{ filteredByDate.length }} entrées · {{ selectedCategory }}
          <span v-if="dateFrom || dateTo"> · période filtrée</span>
        </p>

        <!-- Line chart -->
        <apexchart
          v-if="selectedChart === 'line'"
          type="line"
          height="300"
          :options="lineOptions"
          :series="lineSeries"
        />

        <!-- Bar chart -->
        <apexchart
          v-else-if="selectedChart === 'bar'"
          type="bar"
          height="300"
          :options="barOptions"
          :series="barSeries"
        />

        <!-- Pie chart -->
        <apexchart
          v-else-if="selectedChart === 'pie'"
          type="pie"
          height="300"
          :options="pieOptions"
          :series="pieSeries"
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
const selectedChart    = ref('line')
const dateFrom         = ref('')
const dateTo           = ref('')

const chartTypes = [
  { value: 'line', label: 'Ligne'     },
  { value: 'bar',  label: 'Barres'    },
  { value: 'pie',  label: 'Camembert' }
]

onMounted(() => store.fetchMetrics())

// ── Filtres ──────────────────────────────────────────────────────────

const filteredByCategory = computed(() =>
  store.metrics.filter(m => m.category === selectedCategory.value)
)

const filteredByDate = computed(() => {
  return filteredByCategory.value.filter(m => {
    const d = new Date(m.recorded_at)
    if (dateFrom.value && d < new Date(dateFrom.value)) return false
    if (dateTo.value   && d > new Date(dateTo.value))   return false
    return true
  })
})

function resetDates() {
  dateFrom.value = ''
  dateTo.value   = ''
}

// ── KPI Cards ────────────────────────────────────────────────────────

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

// ── Chart title ───────────────────────────────────────────────────────

const chartTitle = computed(() => {
  const titles = { line: 'Évolution dans le temps', bar: 'Comparaison par métrique', pie: 'Distribution des valeurs' }
  return `${titles[selectedChart.value]} — ${selectedCategory.value}`
})

// ── Line chart ────────────────────────────────────────────────────────

const uniqueNames = computed(() =>
  [...new Set(filteredByDate.value.map(m => m.name))]
)

const lineSeries = computed(() =>
  uniqueNames.value.map(name => ({
    name,
    data: filteredByDate.value
      .filter(m => m.name === name)
      .sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
      .map(m => m.value)
  }))
)

const lineLabels = computed(() =>
  [...new Set(
    filteredByDate.value
      .sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
      .map(m => m.recorded_at)
  )]
)

const lineOptions = computed(() => ({
  chart:   { toolbar: { show: false }, zoom: { enabled: false } },
  stroke:  { curve: 'smooth', width: 2 },
  xaxis:   { categories: lineLabels.value },
  colors:  ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'],
  grid:    { borderColor: '#F3F4F6' },
  legend:  { position: 'top' },
  tooltip: { y: { formatter: val => val.toLocaleString() } }
}))

// ── Bar chart ─────────────────────────────────────────────────────────

const barSeries = computed(() => [{
  name: 'Valeur',
  data: uniqueNames.value.map(name => {
    const entries = filteredByDate.value.filter(m => m.name === name)
    return entries.length
      ? Math.round(entries.reduce((s, m) => s + m.value, 0) / entries.length)
      : 0
  })
}])

const barOptions = computed(() => ({
  chart:       { toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 6, columnWidth: '50%' } },
  xaxis:       { categories: uniqueNames.value },
  colors:      ['#3B82F6'],
  grid:        { borderColor: '#F3F4F6' },
  dataLabels:  { enabled: false },
  tooltip:     { y: { formatter: val => val.toLocaleString() } }
}))

// ── Pie chart ─────────────────────────────────────────────────────────

const pieSeries = computed(() =>
  uniqueNames.value.map(name => {
    const entries = filteredByDate.value.filter(m => m.name === name)
    return entries.length
      ? Math.round(entries.reduce((s, m) => s + m.value, 0) / entries.length)
      : 0
  }).filter(v => v > 0)
)

const pieLabels = computed(() =>
  uniqueNames.value.filter((name, i) => pieSeries.value[i] > 0)
)

const pieOptions = computed(() => ({
  labels:  pieLabels.value,
  colors:  ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
  legend:  { position: 'bottom' },
  tooltip: { y: { formatter: val => val.toLocaleString() } }
}))
</script>
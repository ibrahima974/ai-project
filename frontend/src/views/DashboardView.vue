<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 tracking-tight">Dashboard</h2>
        <p class="text-sm text-gray-400 mt-0.5">Welcome back, {{ username }} 👋</p>
      </div>
      <div class="hidden sm:flex items-center gap-2 bg-white border border-gray-100 rounded-xl px-3 py-2 text-xs text-gray-400 shadow-sm">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        {{ today }}
      </div>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex items-center justify-center h-64">
      <div class="flex flex-col items-center gap-3">
        <div class="w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full animate-spin"/>
        <p class="text-sm text-gray-400">Loading metrics...</p>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-100 text-red-600 rounded-2xl p-4 mb-6 text-sm">
      {{ store.error }}
    </div>

    <div v-else>

      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <KpiCard label="Monthly Revenue"  :value="latestRevenue" unit="€"       :trend="2.4"  />
        <KpiCard label="New Clients"      :value="latestClients" unit="clients" :trend="8.1"  />
        <KpiCard label="Churn Rate"       :value="latestChurn"   unit="%"       :trend="-0.3" />
      </div>

      <!-- Controls -->
      <div class="bg-white border border-gray-100 rounded-2xl p-4 mb-6 shadow-sm">
        <div class="flex flex-wrap items-center gap-3">

          <!-- Category filter -->
          <div class="flex gap-1.5">
            <button
              v-for="cat in categories" :key="cat"
              @click="selectedCategory = cat"
              class="px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all"
              :class="selectedCategory === cat
                ? 'bg-blue-600 text-white shadow-md shadow-blue-200'
                : 'bg-gray-50 text-gray-500 hover:bg-gray-100'"
            >
              {{ cat }}
            </button>
          </div>

          <div class="hidden sm:block h-5 w-px bg-gray-200"/>

          <!-- Date range -->
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <span class="font-medium">From</span>
            <input v-model="dateFrom" type="date"
              class="border border-gray-200 rounded-xl px-2.5 py-1.5 text-xs focus:outline-none focus:border-blue-400 bg-gray-50 focus:bg-white transition-all"/>
            <span class="font-medium">to</span>
            <input v-model="dateTo" type="date"
              class="border border-gray-200 rounded-xl px-2.5 py-1.5 text-xs focus:outline-none focus:border-blue-400 bg-gray-50 focus:bg-white transition-all"/>
            <button @click="resetDates" class="text-blue-500 hover:text-blue-700 text-xs font-medium transition-colors">
              Reset
            </button>
          </div>

          <!-- Chart type -->
          <div class="ml-auto flex gap-1">
            <button
              v-for="type in chartTypes" :key="type.value"
              @click="selectedChart = type.value"
              class="px-3 py-1.5 rounded-xl text-xs font-semibold transition-all"
              :class="selectedChart === type.value
                ? 'bg-gray-900 text-white'
                : 'bg-gray-50 text-gray-500 hover:bg-gray-100'"
            >
              {{ type.label }}
            </button>
          </div>

        </div>
      </div>

      <!-- Chart -->
      <div class="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-sm font-bold text-gray-900">{{ chartTitle }}</h3>
            <p class="text-xs text-gray-400 mt-0.5">
              {{ filteredByDate.length }} entries · {{ selectedCategory }}
              <span v-if="dateFrom || dateTo"> · filtered</span>
            </p>
          </div>
          <div class="w-2 h-2 rounded-full bg-green-400 animate-pulse"/>
        </div>

        <apexchart v-if="selectedChart === 'line'" type="line" height="280" :options="lineOptions" :series="lineSeries"/>
        <apexchart v-else-if="selectedChart === 'bar'" type="bar" height="280" :options="barOptions" :series="barSeries"/>
        <apexchart v-else-if="selectedChart === 'pie'" type="pie" height="280" :options="pieOptions" :series="pieSeries"/>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMetricsStore } from '../stores/metricsStore'
import { useAuthStore } from '../stores/authStore'
import KpiCard from '../components/KpiCard.vue'

const store        = useMetricsStore()
const authStore    = useAuthStore()
const categories   = ['Sales', 'Marketing', 'Support']
const chartTypes   = [{ value:'line', label:'Line' }, { value:'bar', label:'Bar' }, { value:'pie', label:'Pie' }]

const selectedCategory = ref('Sales')
const selectedChart    = ref('line')
const dateFrom         = ref('')
const dateTo           = ref('')

const username = computed(() => authStore.user?.username || 'there')
const today    = computed(() => new Date().toLocaleDateString('en-US', { weekday:'short', month:'short', day:'numeric' }))

onMounted(() => store.fetchMetrics())

const filteredByDate = computed(() =>
  store.metrics
    .filter(m => m.category === selectedCategory.value)
    .filter(m => {
      const d = new Date(m.recorded_at)
      if (dateFrom.value && d < new Date(dateFrom.value)) return false
      if (dateTo.value   && d > new Date(dateTo.value))   return false
      return true
    })
)

function resetDates() { dateFrom.value = ''; dateTo.value = '' }
const latestRevenue = computed(() => { const m = store.metrics.filter(m => m.name === 'Monthly Revenue'); return m.length ? m[0].value.toLocaleString() : '—' })
const latestClients = computed(() => { const m = store.metrics.filter(m => m.name === 'New Clients'); return m.length ? m[0].value : '—' })
const latestChurn   = computed(() => { const m = store.metrics.filter(m => m.name === 'Churn Rate'); return m.length ? m[0].value : '—' })

const uniqueNames  = computed(() => [...new Set(filteredByDate.value.map(m => m.name))])
const chartLabels  = computed(() => [...new Set(filteredByDate.value.sort((a,b) => new Date(a.recorded_at)-new Date(b.recorded_at)).map(m => m.recorded_at))])
const chartTitle   = computed(() => ({ line:'Trend Over Time', bar:'Average by Metric', pie:'Value Distribution' }[selectedChart.value] + ' — ' + selectedCategory.value))

const lineSeries = computed(() => uniqueNames.value.map(name => ({
  name, data: filteredByDate.value.filter(m => m.name === name).sort((a,b) => new Date(a.recorded_at)-new Date(b.recorded_at)).map(m => m.value)
})))

const barSeries = computed(() => [{ name:'Average', data: uniqueNames.value.map(name => {
  const e = filteredByDate.value.filter(m => m.name === name)
  return e.length ? Math.round(e.reduce((s,m) => s+m.value,0)/e.length) : 0
})}])

const pieSeries  = computed(() => uniqueNames.value.map(name => { const e = filteredByDate.value.filter(m => m.name === name); return e.length ? Math.round(e.reduce((s,m) => s+m.value,0)/e.length) : 0 }).filter(v => v > 0))
const pieLabels  = computed(() => uniqueNames.value.filter((_,i) => pieSeries.value[i] > 0))

const baseChart  = { toolbar:{ show:false }, zoom:{ enabled:false }, fontFamily:'inherit' }
const baseColors = ['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6']

const lineOptions = computed(() => ({
  chart: { ...baseChart, type:'line' },
  stroke:{ curve:'smooth', width:2.5 },
  xaxis: { categories: chartLabels.value, labels:{ style:{ fontSize:'11px', colors:'#9CA3AF' } }, axisBorder:{ show:false }, axisTicks:{ show:false } },
  yaxis: { labels:{ style:{ fontSize:'11px', colors:'#9CA3AF' } } },
  colors: baseColors,
  grid:  { borderColor:'#F3F4F6', strokeDashArray:4 },
  legend:{ position:'top', fontSize:'12px' },
  markers:{ size:4, strokeWidth:2, strokeColors:'#fff' },
  tooltip:{ y:{ formatter: v => v.toLocaleString() } }
}))

const barOptions = computed(() => ({
  chart: { ...baseChart, type:'bar' },
  plotOptions:{ bar:{ borderRadius:8, columnWidth:'45%' } },
  xaxis: { categories: uniqueNames.value, labels:{ style:{ fontSize:'11px', colors:'#9CA3AF' } }, axisBorder:{ show:false }, axisTicks:{ show:false } },
  yaxis: { labels:{ style:{ fontSize:'11px', colors:'#9CA3AF' } } },
  colors: baseColors,
  grid:  { borderColor:'#F3F4F6', strokeDashArray:4 },
  dataLabels:{ enabled:false },
  tooltip:{ y:{ formatter: v => v.toLocaleString() } }
}))

const pieOptions = computed(() => ({
  labels: pieLabels.value,
  colors: baseColors,
  legend:{ position:'bottom', fontSize:'12px' },
  dataLabels:{ style:{ fontSize:'11px' } },
  tooltip:{ y:{ formatter: v => v.toLocaleString() } }
}))
</script>
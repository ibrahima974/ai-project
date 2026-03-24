<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 tracking-tight">Metrics</h2>
        <p class="text-sm text-gray-400 mt-0.5">Manage your business KPIs</p>
      </div>
      <button @click="openCreate"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-xl hover:bg-blue-700 transition-all shadow-lg shadow-blue-200">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span class="hidden sm:inline">Add metric</span>
        <span class="sm:hidden">Add</span>
      </button>
    </div>

    <!-- Success -->
    <div v-if="successMsg" class="bg-green-50 border border-green-100 text-green-700 rounded-2xl p-3 mb-4 text-sm font-medium flex items-center gap-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
      {{ successMsg }}
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-2 mb-5">
      <button
        v-for="cat in ['All', 'Sales', 'Marketing', 'Support']" :key="cat"
        @click="selectedCategory = cat"
        class="px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all"
        :class="selectedCategory === cat
          ? 'bg-blue-600 text-white shadow-md shadow-blue-200'
          : 'bg-white border border-gray-100 text-gray-500 hover:bg-gray-50 shadow-sm'"
      >
        {{ cat }}
        <span v-if="cat === 'All'" class="ml-1 opacity-60">({{ store.metrics.length }})</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center h-40 items-center">
      <div class="w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full animate-spin"/>
    </div>

    <!-- Error -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-100 text-red-600 rounded-2xl p-4 text-sm">
      {{ store.error }}
    </div>

    <!-- Empty -->
    <div v-else-if="filtered.length === 0" class="bg-white border border-gray-100 rounded-2xl p-12 text-center shadow-sm">
      <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
      </div>
      <p class="text-sm text-gray-400 font-medium">No metrics for this category</p>
      <button @click="openCreate" class="mt-3 text-blue-600 text-sm font-semibold hover:underline">Add a metric</button>
    </div>

    <!-- Table desktop -->
    <div v-else class="bg-white border border-gray-100 rounded-2xl shadow-sm overflow-hidden">
      <!-- Desktop -->
      <div class="hidden sm:block overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Name</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Value</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Category</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Date</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="m in filtered" :key="m.id" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-5 py-4 font-semibold text-gray-800 text-sm">{{ m.name }}</td>
              <td class="px-5 py-4 text-gray-600 font-mono text-sm">{{ m.value.toLocaleString() }} <span class="text-gray-400">{{ m.unit }}</span></td>
              <td class="px-5 py-4">
                <span class="px-2.5 py-1 rounded-lg text-xs font-semibold"
                  :class="{
                    'bg-blue-50 text-blue-700':   m.category === 'Sales',
                    'bg-green-50 text-green-700': m.category === 'Marketing',
                    'bg-amber-50 text-amber-700': m.category === 'Support'
                  }">
                  {{ m.category }}
                </span>
              </td>
              <td class="px-5 py-4 text-gray-400 text-xs">{{ m.recorded_at }}</td>
              <td class="px-5 py-4">
                <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="openEdit(m)"
                    class="px-2.5 py-1.5 rounded-lg border border-gray-200 text-xs font-medium text-gray-500 hover:border-blue-300 hover:text-blue-600 transition-all">
                    Edit
                  </button>
                  <button @click="remove(m.id)"
                    class="px-2.5 py-1.5 rounded-lg border border-gray-200 text-xs font-medium text-gray-500 hover:border-red-300 hover:text-red-500 transition-all">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mobile cards -->
      <div class="sm:hidden divide-y divide-gray-50">
        <div v-for="m in filtered" :key="m.id" class="p-4">
          <div class="flex items-start justify-between mb-2">
            <div>
              <p class="text-sm font-semibold text-gray-800">{{ m.name }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ m.recorded_at }}</p>
            </div>
            <span class="px-2.5 py-1 rounded-lg text-xs font-semibold"
              :class="{
                'bg-blue-50 text-blue-700':   m.category === 'Sales',
                'bg-green-50 text-green-700': m.category === 'Marketing',
                'bg-amber-50 text-amber-700': m.category === 'Support'
              }">
              {{ m.category }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <p class="text-lg font-bold text-gray-900 font-mono">{{ m.value.toLocaleString() }} <span class="text-sm font-normal text-gray-400">{{ m.unit }}</span></p>
            <div class="flex gap-1">
              <button @click="openEdit(m)" class="px-2.5 py-1.5 rounded-lg border border-gray-200 text-xs text-gray-500 hover:text-blue-600 hover:border-blue-300 transition-all">Edit</button>
              <button @click="remove(m.id)" class="px-2.5 py-1.5 rounded-lg border border-gray-200 text-xs text-gray-500 hover:text-red-500 hover:border-red-300 transition-all">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <MetricModal v-if="showModal" :metric="editingMetric" @close="showModal = false" @saved="handleSaved"/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMetricsStore } from '../stores/metricsStore'
import MetricModal from '../components/MetricModal.vue'

const store            = useMetricsStore()
const showModal        = ref(false)
const editingMetric    = ref(null)
const selectedCategory = ref('All')
const successMsg       = ref('')

onMounted(() => store.fetchMetrics())

const filtered = computed(() =>
  selectedCategory.value === 'All'
    ? store.metrics
    : store.metrics.filter(m => m.category === selectedCategory.value)
)

function openCreate() { editingMetric.value = null; showModal.value = true }
function openEdit(m)  { editingMetric.value = m;    showModal.value = true }

async function handleSaved(data) {
  try {
    if (editingMetric.value) { await store.updateMetric(editingMetric.value.id, data); showSuccess('Metric updated.') }
    else                     { await store.createMetric(data); showSuccess('Metric created.') }
    showModal.value = false
  } catch { alert('An error occurred. Please try again.') }
}

async function remove(id) {
  if (!confirm('Delete this metric?')) return
  await store.deleteMetric(id)
  showSuccess('Metric deleted.')
}

function showSuccess(msg) { successMsg.value = msg; setTimeout(() => successMsg.value = '', 3000) }
</script>
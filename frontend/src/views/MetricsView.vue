<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Métriques</h2>
        <p class="text-gray-400 text-sm mt-0.5">Gère tes KPIs business</p>
      </div>
      <button
        @click="openCreate"
        class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
      >
        + Ajouter
      </button>
    </div>

    <!-- Message succès -->
    <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 mb-4 text-sm">
      {{ successMsg }}
    </div>

    <!-- Filtre -->
    <div class="flex gap-2 mb-4">
      <button
        v-for="cat in ['Toutes', 'Sales', 'Marketing', 'Support']"
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

    <!-- Loading -->
    <div v-if="store.loading" class="flex items-center justify-center h-40">
      <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Erreur -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-200 text-red-600 rounded-lg p-4">
      {{ store.error }}
    </div>

    <!-- Tableau vide -->
    <div v-else-if="filtered.length === 0" class="bg-white rounded-xl border border-gray-200 p-12 text-center">
      <p class="text-gray-400 text-sm">Aucune métrique pour cette catégorie.</p>
      <button @click="openCreate" class="mt-3 text-blue-600 text-sm hover:underline">
        Ajouter une métrique
      </button>
    </div>

    <!-- Tableau -->
    <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-5 py-3 text-gray-500 font-medium">Nom</th>
            <th class="text-left px-5 py-3 text-gray-500 font-medium">Valeur</th>
            <th class="text-left px-5 py-3 text-gray-500 font-medium">Catégorie</th>
            <th class="text-left px-5 py-3 text-gray-500 font-medium">Date</th>
            <th class="text-left px-5 py-3 text-gray-500 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="m in filtered" :key="m.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-5 py-3 font-medium text-gray-900">{{ m.name }}</td>
            <td class="px-5 py-3 text-gray-700">{{ m.value.toLocaleString() }} {{ m.unit }}</td>
            <td class="px-5 py-3">
              <span class="px-2 py-1 rounded-full text-xs font-medium"
                :class="{
                  'bg-blue-50 text-blue-700':   m.category === 'Sales',
                  'bg-green-50 text-green-700': m.category === 'Marketing',
                  'bg-amber-50 text-amber-700': m.category === 'Support'
                }"
              >
                {{ m.category }}
              </span>
            </td>
            <td class="px-5 py-3 text-gray-500">{{ m.recorded_at }}</td>
            <td class="px-5 py-3">
              <div class="flex gap-2">
                <button
                  @click="openEdit(m)"
                  class="text-gray-400 hover:text-blue-600 transition-colors text-xs border border-gray-200 px-2 py-1 rounded"
                >
                  Modifier
                </button>
                <button
                  @click="remove(m.id)"
                  class="text-gray-400 hover:text-red-500 transition-colors text-xs border border-gray-200 px-2 py-1 rounded"
                >
                  Supprimer
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <MetricModal
      v-if="showModal"
      :metric="editingMetric"
      @close="showModal = false"
      @saved="handleSaved"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMetricsStore } from '../stores/metricsStore'
import MetricModal from '../components/MetricModal.vue'

const store            = useMetricsStore()
const showModal        = ref(false)
const editingMetric    = ref(null)
const selectedCategory = ref('Toutes')
const successMsg       = ref('')

onMounted(() => store.fetchMetrics())

const filtered = computed(() =>
  selectedCategory.value === 'Toutes'
    ? store.metrics
    : store.metrics.filter(m => m.category === selectedCategory.value)
)

function openCreate() {
  editingMetric.value = null
  showModal.value     = true
}

function openEdit(metric) {
  editingMetric.value = metric
  showModal.value     = true
}

async function handleSaved(data) {
  try {
    if (editingMetric.value) {
      await store.updateMetric(editingMetric.value.id, data)
      showSuccess('Métrique modifiée avec succès.')
    } else {
      await store.createMetric(data)
      showSuccess('Métrique créée avec succès.')
    }
    showModal.value = false
  } catch {
    alert('Une erreur est survenue. Réessaie.')
  }
}

async function remove(id) {
  if (!confirm('Supprimer cette métrique ?')) return
  await store.deleteMetric(id)
  showSuccess('Métrique supprimée.')
}

function showSuccess(msg) {
  successMsg.value = msg
  setTimeout(() => successMsg.value = '', 3000)
}
</script>
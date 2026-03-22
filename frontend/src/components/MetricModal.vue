<template>
  <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl border border-gray-200 p-6 w-full max-w-md mx-4">

      <h3 class="text-lg font-semibold text-gray-900 mb-5">
        {{ metric ? 'Modifier la métrique' : 'Nouvelle métrique' }}
      </h3>

      <div class="space-y-4">

        <!-- Nom -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
          <input
            v-model="form.name"
            type="text"
            placeholder="ex: Revenu mensuel"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
          />
          <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
        </div>

        <!-- Valeur + Unité -->
        <div class="flex gap-3">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700 mb-1">Valeur</label>
            <input
              v-model="form.value"
              type="number"
              placeholder="ex: 45000"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
            />
            <p v-if="errors.value" class="text-red-500 text-xs mt-1">{{ errors.value }}</p>
          </div>
          <div class="w-28">
            <label class="block text-sm font-medium text-gray-700 mb-1">Unité</label>
            <input
              v-model="form.unit"
              type="text"
              placeholder="€, %, users"
              class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
            />
            <p v-if="errors.unit" class="text-red-500 text-xs mt-1">{{ errors.unit }}</p>
          </div>
        </div>

        <!-- Catégorie -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Catégorie</label>
          <select
            v-model="form.category"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
          >
            <option value="">Choisir une catégorie</option>
            <option value="Sales">Sales</option>
            <option value="Marketing">Marketing</option>
            <option value="Support">Support</option>
          </select>
          <p v-if="errors.category" class="text-red-500 text-xs mt-1">{{ errors.category }}</p>
        </div>

        <!-- Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            v-model="form.recorded_at"
            type="date"
            class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
          />
          <p v-if="errors.recorded_at" class="text-red-500 text-xs mt-1">{{ errors.recorded_at }}</p>
        </div>

      </div>

      <!-- Boutons -->
      <div class="flex gap-3 mt-6">
        <button
          @click="$emit('close')"
          class="flex-1 px-4 py-2 rounded-lg border border-gray-200 text-sm text-gray-600 hover:bg-gray-50 transition-colors"
        >
          Annuler
        </button>
        <button
          @click="submit"
          :disabled="loading"
          class="flex-1 px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {{ loading ? 'Enregistrement...' : metric ? 'Modifier' : 'Créer' }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const props = defineProps({
  metric: { type: Object, default: null }
})

const emit   = defineEmits(['close', 'saved'])
const loading = ref(false)

const form = reactive({
  name:        '',
  value:       '',
  unit:        '',
  category:    '',
  recorded_at: ''
})

const errors = reactive({
  name: '', value: '', unit: '', category: '', recorded_at: ''
})

onMounted(() => {
  if (props.metric) {
    form.name        = props.metric.name
    form.value       = props.metric.value
    form.unit        = props.metric.unit
    form.category    = props.metric.category
    form.recorded_at = props.metric.recorded_at
  }
})

function validate() {
  let valid = true
  errors.name        = ''
  errors.value       = ''
  errors.unit        = ''
  errors.category    = ''
  errors.recorded_at = ''

  if (!form.name.trim())     { errors.name = 'Le nom est obligatoire'          ; valid = false }
  if (form.value === '')     { errors.value = 'La valeur est obligatoire'       ; valid = false }
  if (!form.unit.trim())     { errors.unit = "L'unité est obligatoire"          ; valid = false }
  if (!form.category)        { errors.category = 'La catégorie est obligatoire' ; valid = false }
  if (!form.recorded_at)     { errors.recorded_at = 'La date est obligatoire'   ; valid = false }

  return valid
}

function submit() {
  if (!validate()) return
  emit('saved', {
    name:        form.name.trim(),
    value:       parseFloat(form.value),
    unit:        form.unit.trim(),
    category:    form.category,
    recorded_at: form.recorded_at
  })
}
</script>
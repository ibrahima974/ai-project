<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">

      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">InsightIQ</h1>
        <p class="text-gray-400 text-sm mt-1">AI-Powered Analytics Dashboard</p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl border border-gray-200 p-8">

        <!-- Tabs -->
        <div class="flex mb-6 bg-gray-100 rounded-lg p-1">
          <button
            @click="mode = 'login'"
            class="flex-1 py-2 text-sm font-medium rounded-md transition-colors"
            :class="mode === 'login'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'"
          >
            Se connecter
          </button>
          <button
            @click="mode = 'register'"
            class="flex-1 py-2 text-sm font-medium rounded-md transition-colors"
            :class="mode === 'register'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'"
          >
            Créer un compte
          </button>
        </div>

        <!-- Formulaire -->
        <div class="space-y-4">

          <!-- Username (register seulement) -->
          <div v-if="mode === 'register'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nom d'utilisateur
            </label>
            <input
              v-model="form.username"
              type="text"
              placeholder="ex: Marie Martin"
              class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            />
            <p v-if="errors.username" class="text-red-500 text-xs mt-1">
              {{ errors.username }}
            </p>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="ex: marie@entreprise.com"
              class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            />
            <p v-if="errors.email" class="text-red-500 text-xs mt-1">
              {{ errors.email }}
            </p>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mot de passe
            </label>
            <input
              v-model="form.password"
              type="password"
              placeholder="minimum 6 caractères"
              class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            />
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">
              {{ errors.password }}
            </p>
          </div>

          <!-- Message succès register -->
          <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 rounded-lg p-3 text-sm">
            {{ successMsg }}
          </div>

          <!-- Erreur globale -->
          <div v-if="globalError" class="bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 text-sm">
            {{ globalError }}
          </div>

          <!-- Bouton -->
          <button
            @click="submit"
            :disabled="loading"
            class="w-full py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
          >
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ loading ? 'Chargement...' : mode === 'login' ? 'Se connecter' : 'Créer mon compte' }}
          </button>

        </div>
      </div>

      <p class="text-center text-xs text-gray-400 mt-6">
        InsightIQ — Dashboard Analytics
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router      = useRouter()
const authStore   = useAuthStore()
const mode        = ref('login')
const loading     = ref(false)
const globalError = ref('')
const successMsg  = ref('')

const form   = reactive({ email: '', password: '', username: '' })
const errors = reactive({ email: '', password: '', username: '' })

watch(mode, () => {
  globalError.value = ''
  successMsg.value  = ''
  errors.email      = ''
  errors.password   = ''
  errors.username   = ''
})

function validate() {
  let valid = true
  errors.email    = ''
  errors.password = ''
  errors.username = ''

  if (!form.email.trim())             { errors.email    = "L'email est obligatoire"        ; valid = false }
  else if (!form.email.includes('@')) { errors.email    = "Email invalide"                 ; valid = false }
  if (!form.password.trim())          { errors.password = "Le mot de passe est obligatoire"; valid = false }
  else if (form.password.length < 6)  { errors.password = "6 caractères minimum"           ; valid = false }
  if (mode.value === 'register' && !form.username.trim()) {
    errors.username = "Le nom est obligatoire"; valid = false
  }
  return valid
}

async function submit() {
  if (!validate()) return
  loading.value     = true
  globalError.value = ''
  successMsg.value  = ''

  try {
    if (mode.value === 'login') {
      await authStore.login(form.email, form.password)
      router.push('/')
    } else {
      await authStore.register(form.email, form.username, form.password)
      authStore.logout()
      mode.value       = 'login'
      form.password    = ''
      form.username    = ''
      successMsg.value = 'Compte créé avec succès ! Connecte-toi maintenant.'
    }
  } catch (e) {
    globalError.value = e.response?.data?.detail || 'Une erreur est survenue. Réessaie.'
  } finally {
    loading.value = false
  }
}
</script>
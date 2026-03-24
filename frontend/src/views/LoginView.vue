<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center p-4">
    <div class="w-full max-w-sm">

      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-blue-200">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">InsightIQ</h1>
        <p class="text-sm text-gray-400 mt-1">AI-Powered Analytics Dashboard</p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-xl shadow-gray-200/60 border border-gray-100 p-6">

        <!-- Tabs -->
        <div class="flex mb-6 bg-gray-50 rounded-xl p-1 gap-1">
          <button
            @click="mode = 'login'"
            class="flex-1 py-2 text-xs font-semibold rounded-lg transition-all"
            :class="mode === 'login' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            Sign in
          </button>
          <button
            @click="mode = 'register'"
            class="flex-1 py-2 text-xs font-semibold rounded-lg transition-all"
            :class="mode === 'register' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            Create account
          </button>
        </div>

        <div class="space-y-4">

          <div v-if="mode === 'register'">
            <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Username</label>
            <input v-model="form.username" type="text" placeholder="e.g. John Smith"
              class="w-full border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all bg-gray-50 focus:bg-white"/>
            <p v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Email</label>
            <input v-model="form.email" type="email" placeholder="e.g. john@company.com"
              class="w-full border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all bg-gray-50 focus:bg-white"/>
            <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Password</label>
            <input v-model="form.password" type="password" placeholder="Minimum 6 characters"
              class="w-full border border-gray-200 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all bg-gray-50 focus:bg-white"/>
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
          </div>

          <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 rounded-xl p-3 text-xs font-medium">
            {{ successMsg }}
          </div>
          <div v-if="globalError" class="bg-red-50 border border-red-200 text-red-600 rounded-xl p-3 text-xs">
            {{ globalError }}
          </div>

          <button @click="submit" :disabled="loading"
            class="w-full py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-sm font-semibold rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-blue-200 mt-2">
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>
            {{ loading ? 'Loading...' : mode === 'login' ? 'Sign in' : 'Create account' }}
          </button>

        </div>
      </div>

      <p class="text-center text-xs text-gray-400 mt-6">InsightIQ - Analytics Dashboard</p>
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
const form        = reactive({ email: '', password: '', username: '' })
const errors      = reactive({ email: '', password: '', username: '' })

watch(mode, () => {
  globalError.value = ''
  successMsg.value  = ''
  errors.email = errors.password = errors.username = ''
})

function validate() {
  let valid = true
  errors.email = errors.password = errors.username = ''
  if (!form.email.trim())             { errors.email    = 'Email is required'        ; valid = false }
  else if (!form.email.includes('@')) { errors.email    = 'Invalid email'             ; valid = false }
  if (!form.password.trim())          { errors.password = 'Password is required'     ; valid = false }
  else if (form.password.length < 6)  { errors.password = 'Minimum 6 characters'     ; valid = false }
  if (mode.value === 'register' && !form.username.trim()) { errors.username = 'Name is required'; valid = false }
  return valid
}

async function submit() {
  if (!validate()) return
  loading.value = true
  globalError.value = ''
  successMsg.value = ''
  try {
    if (mode.value === 'login') {
      await authStore.login(form.email, form.password)
      router.push('/')
    } else {
      await authStore.register(form.email, form.username, form.password)
      authStore.logout()
      mode.value = 'login'
      form.password = form.username = ''
      successMsg.value = 'Account created! Sign in now.'
    }
  } catch (e) {
    globalError.value = e.response?.data?.detail || 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
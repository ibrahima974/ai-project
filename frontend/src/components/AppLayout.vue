<template>
  <div class="min-h-screen bg-gray-50 flex">

    <!-- Sidebar -->
    <aside
      class="bg-white border-r border-gray-200 flex flex-col fixed h-full transition-all duration-300 z-10"
      :class="collapsed ? 'w-16' : 'w-64'"
    >
      <!-- Header sidebar -->
      <div class="flex items-center border-b border-gray-200 h-16 px-3 gap-3">
        <button
          @click="collapsed = !collapsed"
          class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors flex-shrink-0"
        >
          <svg class="w-5 h-5 transition-transform duration-300" :class="collapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
          </svg>
        </button>
        <div v-if="!collapsed" class="overflow-hidden">
          <h1 class="text-base font-bold text-gray-900 whitespace-nowrap">InsightIQ</h1>
          <p class="text-xs text-gray-400 whitespace-nowrap">Tableau de bord analytique</p>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-2 py-4 space-y-1">

        <RouterLink
          to="/"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="[
            $route.path === '/'
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-600 hover:bg-gray-100',
            collapsed ? 'justify-center' : ''
          ]"
          :title="collapsed ? 'Tableau de bord' : ''"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          <span v-if="!collapsed" class="whitespace-nowrap">Tableau de bord</span>
        </RouterLink>

        <RouterLink
          to="/metrics"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="[
            $route.path === '/metrics'
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-600 hover:bg-gray-100',
            collapsed ? 'justify-center' : ''
          ]"
          :title="collapsed ? 'Métriques' : ''"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          <span v-if="!collapsed" class="whitespace-nowrap">Métriques</span>
        </RouterLink>

        <RouterLink
          to="/insights"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="[
            $route.path === '/insights'
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-600 hover:bg-gray-100',
            collapsed ? 'justify-center' : ''
          ]"
          :title="collapsed ? 'Insights IA' : ''"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
          </svg>
          <span v-if="!collapsed" class="whitespace-nowrap">Insights IA</span>
        </RouterLink>

      </nav>

      <!-- Footer sidebar -->
      <div class="px-2 py-4 border-t border-gray-200">

        <!-- Infos utilisateur -->
        <div
          class="flex items-center gap-3 px-3 py-2 mb-1 rounded-lg"
          :class="collapsed ? 'justify-center' : ''"
        >
          <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 text-sm font-bold flex-shrink-0">
            {{ userInitial }}
          </div>
          <div v-if="!collapsed" class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ username }}</p>
            <p class="text-xs text-gray-400 truncate">{{ userEmail }}</p>
          </div>
        </div>

        <!-- Bouton déconnexion -->
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-500 hover:bg-red-50 hover:text-red-600 transition-colors"
          :class="collapsed ? 'justify-center' : ''"
          :title="collapsed ? 'Déconnexion' : ''"
        >
          <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          <span v-if="!collapsed" class="whitespace-nowrap">Déconnexion</span>
        </button>

      </div>
    </aside>

    <!-- Contenu principal -->
    <main
      class="flex-1 p-8 transition-all duration-300"
      :class="collapsed ? 'ml-16' : 'ml-64'"
    >
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router    = useRouter()
const authStore = useAuthStore()
const collapsed = ref(false)

const username    = computed(() => authStore.user?.username || 'Utilisateur')
const userEmail   = computed(() => authStore.user?.email || '')
const userInitial = computed(() => username.value.charAt(0).toUpperCase())

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
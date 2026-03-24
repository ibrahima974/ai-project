<template>
  <div class="min-h-screen bg-gray-50 flex">

    <!-- Overlay mobile -->
    <div
      v-if="mobileOpen"
      class="fixed inset-0 bg-black/40 z-20 lg:hidden"
      @click="mobileOpen = false"
    />

    <!-- Sidebar -->
    <aside
      class="bg-white border-r border-gray-100 flex flex-col fixed h-full z-30 transition-all duration-300"
      :class="[
        collapsed ? 'w-16' : 'w-64',
        mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- Header -->
      <div class="flex items-center h-16 px-3 border-b border-gray-100 gap-3">
        <button
          @click="collapsed = !collapsed"
          class="hidden lg:flex w-8 h-8 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-all flex-shrink-0"
        >
          <svg class="w-4 h-4 transition-transform duration-300" :class="collapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
          </svg>
        </button>
        <button
          @click="mobileOpen = false"
          class="lg:hidden w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 flex-shrink-0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        <div v-if="!collapsed" class="overflow-hidden">
          <h1 class="text-sm font-bold text-gray-900 whitespace-nowrap tracking-tight">InsightIQ</h1>
          <p class="text-xs text-gray-400 whitespace-nowrap">Analytics Dashboard</p>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-2 py-4 space-y-0.5">
        <RouterLink
          v-for="link in links" :key="link.to" :to="link.to"
          @click="mobileOpen = false"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all"
          :class="[
            $route.path === link.to
              ? 'bg-blue-50 text-blue-700 shadow-sm'
              : 'text-gray-500 hover:bg-gray-50 hover:text-gray-800',
            collapsed ? 'justify-center' : ''
          ]"
          :title="collapsed ? link.label : ''"
        >
          <component :is="link.icon" class="w-4.5 h-4.5 flex-shrink-0" />
          <span v-if="!collapsed" class="whitespace-nowrap">{{ link.label }}</span>
          <span
            v-if="!collapsed && $route.path === link.to"
            class="ml-auto w-1.5 h-1.5 rounded-full bg-blue-500"
          />
        </RouterLink>
      </nav>

      <!-- Footer -->
      <div class="p-2 border-t border-gray-100">
        <div
          class="flex items-center gap-3 px-3 py-2 mb-1 rounded-xl"
          :class="collapsed ? 'justify-center' : ''"
        >
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
            {{ userInitial }}
          </div>
          <div v-if="!collapsed" class="flex-1 min-w-0">
            <p class="text-xs font-semibold text-gray-800 truncate">{{ username }}</p>
            <p class="text-xs text-gray-400 truncate">{{ userEmail }}</p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs text-gray-400 hover:bg-red-50 hover:text-red-500 transition-all"
          :class="collapsed ? 'justify-center' : ''"
          :title="collapsed ? 'Logout' : ''"
        >
          <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          <span v-if="!collapsed">Logout</span>
        </button>
      </div>
    </aside>

    <!-- Main -->
    <div
      class="flex-1 flex flex-col min-h-screen transition-all duration-300"
      :class="collapsed ? 'lg:ml-16' : 'lg:ml-64'"
    >
      <!-- Top bar mobile -->
      <header class="lg:hidden sticky top-0 z-10 bg-white border-b border-gray-100 px-4 h-14 flex items-center justify-between">
        <button
          @click="mobileOpen = true"
          class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <span class="text-sm font-bold text-gray-900">InsightIQ</span>
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-xs font-bold">
          {{ userInitial }}
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 p-4 lg:p-8">
        <router-view />
      </main>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router    = useRouter()
const authStore = useAuthStore()
const collapsed  = ref(false)
const mobileOpen = ref(false)

const username    = computed(() => authStore.user?.username || 'User')
const userEmail   = computed(() => authStore.user?.email || '')
const userInitial = computed(() => username.value.charAt(0).toUpperCase())

// Icons as render functions
const IconDashboard = { render: () => h('svg', { fill:'none', stroke:'currentColor', viewBox:'0 0 24 24', 'stroke-width':'2', 'stroke-linecap':'round', 'stroke-linejoin':'round' }, [
  h('path', { d:'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
])}
const IconMetrics = { render: () => h('svg', { fill:'none', stroke:'currentColor', viewBox:'0 0 24 24', 'stroke-width':'2', 'stroke-linecap':'round', 'stroke-linejoin':'round' }, [
  h('path', { d:'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])}
const IconInsights = { render: () => h('svg', { fill:'none', stroke:'currentColor', viewBox:'0 0 24 24', 'stroke-width':'2', 'stroke-linecap':'round', 'stroke-linejoin':'round' }, [
  h('path', { d:'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z' })
])}

const links = [
  { to: '/',         label: 'Dashboard',  icon: IconDashboard },
  { to: '/metrics',  label: 'Metrics',    icon: IconMetrics   },
  { to: '/insights', label: 'AI Insights',icon: IconInsights  },
]

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
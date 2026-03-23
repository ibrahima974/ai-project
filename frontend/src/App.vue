<template>
  <AppLayout v-if="authStore.isAuthenticated" />
  <router-view v-else />
</template>

<script setup>
import { useAuthStore } from './stores/authStore'
import AppLayout from './components/AppLayout.vue'

const authStore = useAuthStore()
</script>
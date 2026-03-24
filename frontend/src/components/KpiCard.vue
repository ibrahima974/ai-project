<template>
  <div class="bg-white rounded-2xl border border-gray-100 p-5 hover:shadow-md hover:shadow-gray-100 transition-all">
    <div class="flex items-start justify-between mb-3">
      <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">{{ label }}</p>
      <span
        class="text-xs font-semibold px-2 py-0.5 rounded-full"
        :class="trend >= 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'"
      >
        {{ trend >= 0 ? '▲' : '▼' }} {{ Math.abs(trend) }}%
      </span>
    </div>
    <p class="text-2xl font-bold text-gray-900 tracking-tight">
      {{ value }}<span class="text-sm font-medium text-gray-400 ml-1">{{ unit }}</span>
    </p>
    <p class="text-xs text-gray-400 mt-1">vs last month</p>
  </div>
</template>

<script setup>
defineProps({ label: String, value: [String, Number], unit: String, trend: Number })
</script>
<template>
  <div class="bg-white rounded-xl border border-gray-200 p-5">
    <p class="text-sm text-gray-500 mb-1">{{ label }}</p>
    <p class="text-2xl font-bold text-gray-900">
      {{ value }} <span class="text-base font-normal text-gray-400">{{ unit }}</span>
    </p>
    <p
      class="text-sm mt-1 font-medium"
      :class="trend >= 0 ? 'text-green-600' : 'text-red-500'"
    >
      {{ trend >= 0 ? '▲' : '▼' }} {{ Math.abs(trend) }}% vs mois dernier
    </p>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  unit:  String,
  trend: Number
})
</script>
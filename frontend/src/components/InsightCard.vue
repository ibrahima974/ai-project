<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6">
    <div class="flex items-start justify-between mb-3">
      <div>
        <h3 class="text-base font-semibold text-gray-900">{{ insight.title }}</h3>
        <p class="text-xs text-gray-400 mt-0.5">
          {{ new Date(insight.generated_at).toLocaleDateString('fr-FR', {
            day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
          }) }}
        </p>
      </div>
      <span class="px-2 py-1 rounded-full text-xs font-medium"
        :class="{
          'bg-blue-50 text-blue-700':   insight.category === 'Sales',
          'bg-green-50 text-green-700': insight.category === 'Marketing',
          'bg-amber-50 text-amber-700': insight.category === 'Support'
        }"
      >
        {{ insight.category }}
      </span>
    </div>

    <div class="text-sm text-gray-600 leading-relaxed whitespace-pre-line">
      {{ insight.content }}
    </div>
  </div>
</template>

<script setup>
defineProps({ insight: Object })
</script>
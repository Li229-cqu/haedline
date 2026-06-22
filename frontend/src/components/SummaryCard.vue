<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  content: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <section class="summary-card">
    <h3>{{ title }}</h3>
    <p>{{ content }}</p>
  </section>
</template>

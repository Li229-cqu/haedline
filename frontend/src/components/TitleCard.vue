<script setup>
defineProps({
  titles: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <section>
    <h3>候选标题</h3>
    <el-tag v-for="title in titles" :key="title" class="title-tag">{{ title }}</el-tag>
  </section>
</template>

<style scoped>
.title-tag {
  margin: 0 8px 8px 0;
}
</style>

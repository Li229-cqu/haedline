<script setup>
import ResultPanel from '../components/ResultPanel.vue'
import TextInputPanel from '../components/TextInputPanel.vue'
import { useNewsAnalysis } from '../composables/useNewsAnalysis'


const { text, result, analyzing, uploading, uploadFile, analyze } = useNewsAnalysis()
</script>

<template>
  <section class="page-container">
    <TextInputPanel
      v-model:text="text"
      :uploading="uploading"
      :analyzing="analyzing"
      @upload="uploadFile"
      @analyze="analyze"
    />
    <section v-if="result" class="result-section">
      <ResultPanel :result="result" />
    </section>
  </section>
</template>

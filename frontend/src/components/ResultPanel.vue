<script setup>
import SummaryCard from './SummaryCard.vue'
import TitleCard from './TitleCard.vue'

defineProps({
  result: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <el-card>
    <template #header>分析结果</template>
    <el-alert :title="`新闻记录 ID：${result.news_id}`" type="success" :closable="false" show-icon />
    <el-descriptions class="text-info" :column="3" border>
      <el-descriptions-item label="字数">{{ result.text_info.word_count }}</el-descriptions-item>
      <el-descriptions-item label="句子数">{{ result.text_info.sentence_count }}</el-descriptions-item>
      <el-descriptions-item label="段落数">{{ result.text_info.paragraph_count }}</el-descriptions-item>
    </el-descriptions>
    <SummaryCard title="短摘要" :content="result.summaries.short" />
    <SummaryCard title="长摘要" :content="result.summaries.long" />
    <TitleCard :titles="result.titles" />
  </el-card>
</template>

<style scoped>
.text-info {
  margin-top: 16px;
}
</style>

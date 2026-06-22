<script setup>
defineProps({
  text: {
    type: String,
    default: '',
  },
  uploading: Boolean,
  analyzing: Boolean,
})

const emit = defineEmits(['update:text', 'upload', 'analyze'])

function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (file) emit('upload', file)
  event.target.value = ''
}
</script>

<template>
  <el-card>
    <template #header>新闻文本输入</template>
    <el-input
      :model-value="text"
      type="textarea"
      :rows="10"
      placeholder="请输入或粘贴一篇新闻正文"
      @update:model-value="emit('update:text', $event)"
    />
    <div class="action-row">
      <label class="upload-label">
        <el-button :loading="uploading" :disabled="analyzing" plain type="primary">
          上传 txt/docx
        </el-button>
        <input type="file" accept=".txt,.docx" :disabled="uploading || analyzing" @change="handleFileChange" />
      </label>
      <el-button type="primary" :loading="analyzing" :disabled="uploading" @click="emit('analyze')">
        开始生成
      </el-button>
    </div>
  </el-card>
</template>

<style scoped>
.action-row {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.upload-label input {
  display: none;
}
</style>

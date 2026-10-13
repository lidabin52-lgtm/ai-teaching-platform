<template>
  <div class="code-editor">
    <div class="editor-toolbar">
      <span class="file-name">{{ fileName }}</span>
      <div class="toolbar-actions">
        <button @click="formatCode" title="格式化代码">格式化</button>
        <button @click="copyCode" title="复制代码">复制</button>
        <button @click="clearCode" title="清空">清空</button>
      </div>
    </div>
    <div class="editor-wrapper">
      <div class="line-numbers">
        <div v-for="n in lineCount" :key="n" class="line-number">{{ n }}</div>
      </div>
      <textarea
        ref="textareaRef"
        v-model="localCode"
        class="code-textarea"
        :placeholder="placeholder"
        @input="handleInput"
        @keydown="handleKeydown"
        @scroll="syncScroll"
        spellcheck="false"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'html'
  },
  fileName: {
    type: String,
    default: 'index.html'
  },
  placeholder: {
    type: String,
    default: '在此编写代码...'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const textareaRef = ref(null)
const localCode = ref(props.modelValue)

// 计算行数
const lineCount = computed(() => {
  return (localCode.value || '').split('\n').length
})

// 监听外部值变化
watch(() => props.modelValue, (newVal) => {
  if (newVal !== localCode.value) {
    localCode.value = newVal
  }
})

// 处理输入
const handleInput = () => {
  emit('update:modelValue', localCode.value)
  emit('change', localCode.value)
}

// 处理键盘事件（Tab缩进）
const handleKeydown = (e) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    const textarea = textareaRef.value
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    
    // 插入两个空格作为缩进
    const value = localCode.value
    localCode.value = value.substring(0, start) + '  ' + value.substring(end)
    
    // 恢复光标位置
    nextTick(() => {
      textarea.selectionStart = textarea.selectionEnd = start + 2
    })
    
    emit('update:modelValue', localCode.value)
    emit('change', localCode.value)
  }
}

// 同步滚动
const syncScroll = () => {
  const textarea = textareaRef.value
  const lineNumbers = textarea.parentElement.querySelector('.line-numbers')
  if (lineNumbers) {
    lineNumbers.scrollTop = textarea.scrollTop
  }
}

// 格式化代码（简单实现）
const formatCode = () => {
  try {
    if (props.language === 'json') {
      localCode.value = JSON.stringify(JSON.parse(localCode.value), null, 2)
      emit('update:modelValue', localCode.value)
      emit('change', localCode.value)
      ElMessage.success('格式化完成')
    } else {
      ElMessage.info('当前语言暂不支持自动格式化')
    }
  } catch (e) {
    ElMessage.error('格式化失败：' + e.message)
  }
}

// 复制代码
const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(localCode.value)
    ElMessage.success('已复制到剪贴板')
  } catch (e) {
    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = localCode.value
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('已复制到剪贴板')
  }
}

// 清空代码
const clearCode = () => {
  localCode.value = ''
  emit('update:modelValue', localCode.value)
  emit('change', localCode.value)
  ElMessage.success('已清空')
}

// 聚焦编辑器
const focus = () => {
  textareaRef.value?.focus()
}

// 设置内容
const setContent = (content) => {
  localCode.value = content
  emit('update:modelValue', content)
  emit('change', content)
}

// 获取内容
const getContent = () => {
  return localCode.value
}

defineExpose({
  focus,
  setContent,
  getContent
})

onMounted(() => {
  focus()
})
</script>

<style scoped>
.code-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #1e1e1e;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #2d2d30;
  border-bottom: 1px solid #404040;
}

.file-name {
  color: #cccccc;
  font-size: 13px;
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

.toolbar-actions button {
  padding: 4px 12px;
  font-size: 12px;
  color: #cccccc;
  background: #3c3c3c;
  border: 1px solid #555;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.toolbar-actions button:hover {
  background: #505050;
  border-color: #666;
}

.editor-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.line-numbers {
  width: 50px;
  padding: 16px 8px;
  background: #252526;
  color: #858585;
  font-size: 14px;
  line-height: 1.5;
  text-align: right;
  overflow: hidden;
  user-select: none;
  border-right: 1px solid #404040;
}

.line-number {
  height: 21px;
}

.code-textarea {
  flex: 1;
  padding: 16px;
  background: #1e1e1e;
  color: #d4d4d4;
  border: none;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  tab-size: 2;
  white-space: pre;
  overflow-wrap: normal;
  overflow-x: auto;
}

.code-textarea::placeholder {
  color: #6a6a6a;
}

.code-textarea::-webkit-scrollbar {
  width: 14px;
  height: 14px;
}

.code-textarea::-webkit-scrollbar-track {
  background: #1e1e1e;
}

.code-textarea::-webkit-scrollbar-thumb {
  background: #424242;
  border: 3px solid #1e1e1e;
  border-radius: 7px;
}

.code-textarea::-webkit-scrollbar-thumb:hover {
  background: #4f4f4f;
}

.code-textarea::-webkit-scrollbar-corner {
  background: #1e1e1e;
}
</style>

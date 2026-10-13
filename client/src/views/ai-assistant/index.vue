<template>
  <!-- AI助手：对话式交互界面 -->
  <div class="ai-assistant-page">
    <h2 class="page-title">AI 智能助手</h2>
    <el-card class="chat-container">
      <!-- 对话消息区域 -->
      <div class="chat-messages" ref="messagesRef">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message-item', msg.role === 'user' ? 'message-user' : 'message-ai']"
        >
          <div class="message-avatar">
            {{ msg.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div class="message-bubble" v-html="msg.content"></div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="输入你的问题，例如：请解释Vue 3的组合式API..."
          @keydown.enter.ctrl="handleSend"
        />
        <el-button type="primary" @click="handleSend" :loading="loading">
          发送 (Ctrl+Enter)
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

// 对话消息列表
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    content: '你好！我是AI教学助手，可以帮你解答前端开发问题、分析代码、推荐学习路径。请问有什么可以帮你的？',
  },
])

const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref(null)

/**
 * 发送消息
 */
async function handleSend() {
  if (!inputMessage.value.trim() || loading.value) return

  // 添加用户消息
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
  })

  const question = inputMessage.value
  inputMessage.value = ''
  loading.value = true

  // TODO: 调用AI接口获取回复
  setTimeout(() => {
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: '这是一个示例回复。AI服务对接后，这里将显示DeepSeek的智能回复。',
    })
    loading.value = false
    scrollToBottom()
  }, 1000)

  await nextTick()
  scrollToBottom()
}

/**
 * 滚动到消息底部
 */
function scrollToBottom() {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}
</script>

<style scoped lang="scss">
.ai-assistant-page {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  margin-bottom: 24px;
  color: $text-primary;
}

.chat-container {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
  gap: 12px;

  &.message-user {
    flex-direction: row-reverse;
  }
}

.message-avatar {
  font-size: 32px;
  flex-shrink: 0;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: $border-radius-md;
  line-height: 1.6;
  word-break: break-word;
}

.message-user .message-bubble {
  background-color: $primary-color;
  color: #fff;
}

.message-ai .message-bubble {
  background-color: #f4f4f5;
  color: $text-primary;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 12px;
  align-items: flex-end;

  .el-input {
    flex: 1;
  }
}
</style>

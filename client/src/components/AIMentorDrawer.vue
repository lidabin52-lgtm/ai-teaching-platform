<template>
  <!-- AI导师侧边栏抽屉组件 -->
  <el-drawer
    v-model="visible"
    title=""
    :size="420"
    direction="rtl"
    :show-close="true"
    :close-on-click-modal="false"
    class="mentor-drawer"
    destroy-on-close
  >
    <!-- 自定义头部 -->
    <template #header>
      <div class="drawer-header">
        <div class="header-info">
          <div class="ai-avatar">🤖</div>
          <div class="header-text">
            <h3>AI导师 · 小智</h3>
            <p class="context-hint" v-if="challengeTitle">
              正在闯关：{{ challengeTitle }}
            </p>
            <p class="context-hint" v-else>
              随时为你解答前端问题
            </p>
          </div>
        </div>
        <el-button
          type="danger"
          text
          size="small"
          @click="clearChat"
        >
          清空对话
        </el-button>
      </div>
    </template>

    <!-- 聊天消息区域 -->
    <div class="chat-body" ref="chatBodyRef">
      <!-- 欢迎消息 -->
      <div v-if="messages.length === 0" class="welcome-area">
        <div class="welcome-icon">🤖</div>
        <h4>你好，我是AI导师小智！</h4>
        <p>在闯关过程中遇到任何问题，都可以随时问我。</p>
        <div class="quick-questions">
          <div
            v-for="q in defaultQuestions"
            :key="q"
            class="quick-btn"
            @click="sendQuickQuestion(q)"
          >
            {{ q }}
          </div>
        </div>
      </div>

      <!-- 消息列表 -->
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['chat-message', msg.role]"
      >
        <!-- AI消息 -->
        <template v-if="msg.role === 'assistant'">
          <div class="msg-avatar ai">🤖</div>
          <div class="msg-bubble ai">
            <div class="msg-content markdown-body" v-html="renderMarkdown(msg.content)"></div>
            <div v-if="msg.referenced_knowledge?.length" class="knowledge-ref">
              <el-icon><Reading /></el-icon>
              <span>参考了 {{ msg.referenced_knowledge.length }} 篇知识库文档</span>
            </div>
          </div>
        </template>

        <!-- 用户消息 -->
        <template v-else>
          <div class="msg-bubble user">
            <div class="msg-content">{{ msg.content }}</div>
          </div>
          <div class="msg-avatar user">👤</div>
        </template>
      </div>

      <!-- 加载动画 -->
      <div v-if="isLoading" class="chat-message assistant">
        <div class="msg-avatar ai">🤖</div>
        <div class="msg-bubble ai typing">
          <div class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷提问 + 输入区域 -->
    <div class="chat-footer">
      <!-- 快捷提问按钮 -->
      <div class="quick-bar" v-if="messages.length > 0">
        <el-button
          v-for="q in quickQuestions"
          :key="q"
          size="small"
          round
          @click="sendQuickQuestion(q)"
        >
          {{ q }}
        </el-button>
      </div>

      <!-- 输入框 -->
      <div class="input-area">
        <el-input
          ref="inputRef"
          v-model="inputText"
          type="textarea"
          :rows="2"
          :autosize="{ minRows: 1, maxRows: 4 }"
          placeholder="输入你的问题..."
          resize="none"
          @keydown.enter.exact="handleSend"
          @keydown.enter.shift.exact="() => {}"
        />
        <el-button
          type="primary"
          :icon="Promotion"
          :disabled="!inputText.trim() || isLoading"
          :loading="isLoading"
          circle
          @click="handleSend"
        />
      </div>
      <div class="input-hint">按 Enter 发送，Shift+Enter 换行</div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { Promotion, Reading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  challengeId: {
    type: Number,
    default: null
  },
  challengeTitle: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== 响应式数据 ==========
const visible = ref(false)
const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const chatBodyRef = ref(null)
const inputRef = ref(null)

// 预设快捷提问
const defaultQuestions = [
  '这段代码哪里错了？',
  '这个概念能再解释一下吗？',
  '给我一个提示吧',
  '如何优化这段代码？'
]

const quickQuestions = [
  '这段代码哪里错了？',
  '这个概念能再解释一下吗？',
  '给我一个提示吧'
]

// ========== 监听 ==========
watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(() => visible.value, (val) => {
  emit('update:modelValue', val)
  if (val) {
    nextTick(() => {
      inputRef.value?.focus?.()
    })
  }
})

// ========== 方法 ==========

/** 渲染Markdown */
const renderMarkdown = (text) => {
  if (!text) return ''
  const html = marked(text || '')
  return DOMPurify.sanitize(html)
}

/** 发送快捷提问 */
const sendQuickQuestion = (question) => {
  inputText.value = question
  handleSend()
}

/** 发送消息 */
const handleSend = async () => {
  const text = inputText.value.trim()
  if (!text || isLoading.value) return

  // 添加用户消息
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: text
  })

  inputText.value = ''
  isLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    // 调用后端API
    // const res = await fetch('/api/mentor/chat', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Authorization': `Bearer ${localStorage.getItem('token')}`
    //   },
    //   body: JSON.stringify({
    //     message: text,
    //     challenge_id: props.challengeId
    //   })
    // })
    // const data = await res.json()
    // messages.value.push({ id: Date.now(), role: 'assistant', content: data.data.content })

    // Mock回复
    await new Promise(resolve => setTimeout(resolve, 1200))
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: generateMockReply(text),
      referenced_knowledge: [1, 2]
    })
  } catch (error) {
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: '抱歉，我暂时无法回答。请稍后再试，或尝试完成更多闯关练习来探索答案。'
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

/** 生成Mock回复 */
const generateMockReply = (question) => {
  const q = question.toLowerCase()

  if (q.includes('错误') || q.includes('哪里错')) {
    return `让我来帮你分析一下代码中的问题：

1. **检查HTML结构**：确保所有标签都正确闭合
2. **查看CSS选择器**：确认选择器是否正确匹配目标元素
3. **验证JavaScript逻辑**：检查变量是否在使用前已声明

💡 **建议**：你可以打开浏览器的开发者工具（F12），查看Console面板中是否有报错信息，这能帮助你快速定位问题。

如果还是无法解决，可以把你的代码发给我，我帮你具体分析。`
  }

  if (q.includes('解释') || q.includes('概念') || q.includes('什么')) {
    return `好的，让我为你详细解释一下：

这个概念在前端开发中非常重要。简单来说：

- **核心思想**：通过合理的方式组织代码结构，提高可维护性
- **实际应用**：在实际项目中，你会经常用到这个知识点
- **学习建议**：建议通过闯关练习来巩固理解

📚 你可以在知识库中找到更详细的教程文档。完成更多关卡后，你会有更深的理解！`
  }

  if (q.includes('提示') || q.includes('hint')) {
    return `好的，给你一个小提示 💡：

> 仔细阅读关卡需求描述中的第2条要求，注意属性名称的拼写。

不要直接看答案哦！自己思考出来的解决方案印象更深刻。如果实在卡住了，可以再问我更具体的问题。`
  }

  if (q.includes('优化')) {
    return `关于代码优化，这里有几个方向：

1. **性能优化**：减少DOM操作次数，使用事件委托
2. **代码质量**：提取重复代码为函数，使用有意义的变量名
3. **最佳实践**：遵循语义化HTML规范，添加适当的注释
4. **用户体验**：添加过渡动画，优化交互反馈

你目前代码中最大的优化空间在于__结构组织__，建议先从这方面入手。`
  }

  return `收到你的问题！让我来帮你分析：

这是一个很好的问题。在前端开发中，理解这个概念对于写出高质量的代码非常重要。

**关键要点**：
- 注意代码的规范性和可读性
- 确保功能完整实现
- 考虑边界情况和异常处理

如果你能告诉我更具体的场景或贴出相关代码，我可以给你更有针对性的建议。继续加油！💪`
}

/** 滚动到底部 */
const scrollToBottom = () => {
  if (chatBodyRef.value) {
    chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
  }
}

/** 清空对话 */
const clearChat = () => {
  messages.value = []
  ElMessage.success('对话已清空')
}
</script>

<style scoped lang="scss">
.mentor-drawer {
  :deep(.el-drawer__header) {
    padding: 16px 20px;
    margin-bottom: 0;
    border-bottom: 1px solid #EBEEF5;
  }

  :deep(.el-drawer__body) {
    padding: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
}

// 头部
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 42px;
  height: 42px;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ECF5FF, #D9ECFF);
  border-radius: 50%;
}

.header-text {
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 2px 0;
  }
}

.context-hint {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

// 聊天区域
.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #F5F7FA;
}

// 欢迎区域
.welcome-area {
  text-align: center;
  padding: 40px 20px;
}

.welcome-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.welcome-area h4 {
  font-size: 18px;
  color: #303133;
  margin: 0 0 8px 0;
}

.welcome-area p {
  font-size: 14px;
  color: #909399;
  margin: 0 0 24px 0;
}

.quick-questions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-btn {
  padding: 12px 16px;
  background: #fff;
  border: 1px solid #DCDFE6;
  border-radius: 8px;
  font-size: 13px;
  color: #409EFF;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #ECF5FF;
    border-color: #409EFF;
    transform: translateX(4px);
  }
}

// 消息样式
.chat-message {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;

  &.user {
    flex-direction: row-reverse;
  }
}

.msg-avatar {
  width: 36px;
  height: 36px;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;

  &.ai {
    background: #fff;
  }

  &.user {
    background: #409EFF;
  }
}

.msg-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.7;

  &.ai {
    background: #fff;
    color: #303133;
    border-top-left-radius: 4px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  }

  &.user {
    background: #409EFF;
    color: #fff;
    border-top-right-radius: 4px;
  }
}

.msg-content {
  word-break: break-word;
}

// Markdown样式
.markdown-body {
  p { margin: 0 0 8px 0; &:last-child { margin-bottom: 0; } }
  code {
    background: #F0F0F0;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 13px;
    font-family: Consolas, monospace;
    color: #C7254E;
  }
  pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 8px 0;
    code { background: none; color: inherit; padding: 0; }
  }
  ul, ol { padding-left: 20px; margin: 8px 0; }
  li { margin-bottom: 4px; }
  strong { color: #303133; }
  blockquote {
    border-left: 3px solid #409EFF;
    padding-left: 12px;
    margin: 8px 0;
    color: #606266;
    background: #F5F7FA;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
  }
}

// 知识库引用
.knowledge-ref {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #EBEEF5;
  font-size: 12px;
  color: #909399;

  .el-icon { color: #409EFF; }
}

// 打字动画
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;

  span {
    width: 8px;
    height: 8px;
    background: #C0C4CC;
    border-radius: 50%;
    animation: typing 1.4s ease infinite;

    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-6px); opacity: 1; }
}

// 底部输入区域
.chat-footer {
  border-top: 1px solid #EBEEF5;
  background: #fff;
  padding: 12px 16px;
}

.quick-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  overflow-x: auto;
  padding-bottom: 4px;

  .el-button {
    flex-shrink: 0;
    font-size: 12px;
  }
}

.input-area {
  display: flex;
  gap: 10px;
  align-items: flex-end;

  .el-input {
    flex: 1;
  }

  :deep(.el-textarea__inner) {
    border-radius: 8px;
  }
}

.input-hint {
  text-align: right;
  font-size: 11px;
  color: #C0C4CC;
  margin-top: 6px;
}
</style>

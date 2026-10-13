<template>
  <!-- 技能闯关主页面 -->
  <div class="challenge-page">
    <!-- 顶部：关卡信息栏 -->
    <header class="challenge-header">
      <div class="header-left">
        <el-button
          type="info"
          text
          @click="showSkillTree = true"
        >
          <el-icon><Map-Location /></el-icon>
          技能地图
        </el-button>
        <div class="challenge-info" v-if="currentChallenge">
          <h2 class="challenge-title">{{ currentChallenge.title }}</h2>
          <div class="challenge-meta">
            <el-tag
              :color="difficultyColor"
              effect="dark"
              size="small"
              class="difficulty-tag"
            >
              {{ difficultyBadge }}
            </el-tag>
            <span class="meta-item">
              <el-icon><Timer /></el-icon>
              {{ currentChallenge.timeLimit }}分钟
            </span>
            <span class="meta-item">
              <el-icon><Star-Filled /></el-icon>
              目标 {{ currentChallenge.minStars }}星
            </span>
          </div>
        </div>
      </div>

      <div class="header-right">
        <div v-if="bestStars > 0" class="best-result">
          <span class="best-label">最佳成绩</span>
          <div class="best-stars">
            <span
              v-for="n in 3"
              :key="n"
              class="star"
              :class="{ filled: n <= bestStars }"
            >★</span>
          </div>
        </div>
        <el-button
          type="primary"
          size="large"
          :loading="isSubmitting"
          :disabled="!canSubmit"
          @click="handleSubmit"
        >
          <el-icon><Upload /></el-icon>
          提交审判
        </el-button>
      </div>
    </header>

    <!-- 主体区域 -->
    <main class="challenge-main">
      <!-- 左侧：关卡需求描述 -->
      <aside class="challenge-sidebar left">
        <div class="panel-header">
          <el-icon><Document /></el-icon>
          <span>关卡需求</span>
        </div>
        <div class="panel-content markdown-body" v-if="currentChallenge">
          <div v-html="renderedDescription"></div>
        </div>
        <div v-else class="panel-loading">
          <el-skeleton :rows="10" animated />
        </div>
      </aside>

      <!-- 中间：代码编辑器 -->
      <section class="challenge-editor">
        <div class="panel-header">
          <el-icon><Edit-Pen /></el-icon>
          <span>代码编辑器</span>
          <div class="editor-actions">
            <el-button
              type="warning"
              size="small"
              text
              @click="handleReset"
            >
              <el-icon><Refresh-Right /></el-icon>
              重置
            </el-button>
            <el-button
              type="info"
              size="small"
              text
              @click="handleCallMentor"
            >
              <el-icon><Chat-Dot-Square /></el-icon>
              呼叫导师
            </el-button>
          </div>
        </div>
        <div class="editor-container">
          <CodeEditor
            ref="codeEditorRef"
            v-model="localCode"
            :language="currentChallenge?.language || 'html'"
            :file-name="currentChallenge?.title || 'index.html'"
            @change="handleCodeChange"
          />
        </div>
      </section>

      <!-- 右侧：实时预览 -->
      <aside class="challenge-sidebar right">
        <div class="panel-header">
          <el-icon><View /></el-icon>
          <span>实时预览</span>
          <el-tag size="small" type="info">300ms 自动刷新</el-tag>
        </div>
        <div class="preview-container">
          <iframe
            ref="previewRef"
            :srcdoc="previewContent"
            sandbox="allow-scripts"
            class="preview-frame"
          ></iframe>
        </div>
      </aside>
    </main>

    <!-- 技能树抽屉 -->
    <el-drawer
      v-model="showSkillTree"
      title="技能闯关地图"
      size="400px"
      direction="ltr"
    >
      <SkillTree
        :challenges="challengeList"
        :current-challenge-id="currentChallenge?.id"
        @select="handleSelectChallenge"
      />
    </el-drawer>

    <!-- 审判结果弹窗 -->
    <JudgeResultModal
      v-model="showJudgeModal"
      :result="judgeResult || {}"
      @retry="handleRetry"
      @next="handleNext"
      @ask-mentor="handleCallMentor"
    />

    <!-- AI导师抽屉 -->
    <el-drawer
      v-model="showMentor"
      title="AI导师"
      size="450px"
      direction="rtl"
    >
      <div class="mentor-chat">
        <div class="chat-messages" ref="chatMessagesRef">
          <div
            v-for="msg in chatMessages"
            :key="msg.id"
            :class="['message', msg.role]"
          >
            <div class="message-avatar">
              {{ msg.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="mentorMessage"
            type="textarea"
            :rows="3"
            placeholder="输入你的问题，例如：请帮我看看这段代码有什么问题..."
            @keydown.enter.ctrl="sendMentorMessage"
          />
          <el-button
            type="primary"
            @click="sendMentorMessage"
            :loading="isSendingMessage"
          >
            发送 (Ctrl+Enter)
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useChallengeStore } from '@/store/challenge'
import { ElMessage } from 'element-plus'
import {
  MapLocation, Timer, StarFilled, Upload, Document,
  EditPen, RefreshRight, ChatDotSquare, View
} from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import SkillTree from '@/components/SkillTree.vue'
import JudgeResultModal from '@/components/JudgeResultModal.vue'
import CodeEditor from '@/components/CodeEditor.vue'

// ========== 路由和状态 ==========
const route = useRoute()
const router = useRouter()
const store = useChallengeStore()

const {
  currentChallenge,
  challengeList,
  editorCode,
  isSubmitting,
  isLoading,
  judgeResult,
  showJudgeModal,
  difficultyColor,
  difficultyBadge,
  canSubmit,
  bestStars
} = storeToRefs(store)

// ========== 响应式数据 ==========
const codeEditorRef = ref(null)
const previewRef = ref(null)
const showSkillTree = ref(false)
const showMentor = ref(false)
const mentorMessage = ref('')
const isSendingMessage = ref(false)
const chatMessages = ref([
  { id: 1, role: 'assistant', content: '你好！我是你的AI导师。在闯关过程中有任何问题都可以问我哦！' }
])
const chatMessagesRef = ref(null)
const localCode = ref('')

let debounceTimer = null

// ========== 计算属性 ==========
const renderedDescription = computed(() => {
  if (!currentChallenge.value?.description) return ''
  const html = marked(currentChallenge.value.description)
  return DOMPurify.sanitize(html)
})

const previewContent = computed(() => {
  return editorCode.value || '<!DOCTYPE html><html><body></body></html>'
})

// ========== 方法 ==========

// 初始化代码
const initCode = () => {
  localCode.value = editorCode.value
}

// 处理代码变化
const handleCodeChange = (code) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    store.updateCode(code)
  }, 300)
}

// 加载关卡数据
const loadChallenge = async () => {
  const challengeId = parseInt(route.params.id)
  if (!challengeId) {
    ElMessage.error('关卡ID无效')
    return
  }

  try {
    await store.loadChallengeDetail(challengeId)
    await store.loadChallengeList()
    localCode.value = editorCode.value
  } catch (error) {
    ElMessage.error('加载关卡失败: ' + error.message)
  }
}

// 提交代码
const handleSubmit = async () => {
  if (!canSubmit.value) {
    ElMessage.warning('代码不能为空')
    return
  }

  try {
    await store.submitCode()
    ElMessage.success('审判完成！')
  } catch (error) {
    ElMessage.error('提交失败: ' + error.message)
  }
}

// 重置代码
const handleReset = () => {
  store.resetCode()
  localCode.value = editorCode.value
  ElMessage.success('代码已重置')
}

// 呼叫导师
const handleCallMentor = () => {
  showMentor.value = true
}

// 发送导师消息
const sendMentorMessage = async () => {
  if (!mentorMessage.value.trim()) return

  const message = mentorMessage.value.trim()
  chatMessages.value.push({
    id: Date.now(),
    role: 'user',
    content: message
  })

  mentorMessage.value = ''
  isSendingMessage.value = true

  // 滚动到底部
  await nextTick()
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }

  // 模拟AI回复
  setTimeout(() => {
    chatMessages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: `关于「${message.substring(0, 20)}...」，我的建议是：\n\n这是一个很好的问题！建议你仔细阅读关卡需求，注意代码的规范性。如果需要更具体的帮助，请告诉我你遇到了什么困难。`
    })
    isSendingMessage.value = false

    nextTick(() => {
      if (chatMessagesRef.value) {
        chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
      }
    })
  }, 1000)
}

// 选择关卡
const handleSelectChallenge = (challenge) => {
  showSkillTree.value = false
  if (challenge.id !== currentChallenge.value?.id) {
    router.push(`/challenge/${challenge.id}`)
  }
}

// 再试一次
const handleRetry = () => {
  // 保持当前页面，用户可以修改代码后重新提交
  ElMessage.info('请修改代码后再次提交')
}

// 下一关
const handleNext = () => {
  const next = store.getNextChallenge()
  if (next) {
    router.push(`/challenge/${next.id}`)
  } else {
    ElMessage.success('恭喜你完成了所有关卡！')
  }
}

// ========== 生命周期 ==========
onMounted(() => {
  loadChallenge()
})

onUnmounted(() => {
  clearTimeout(debounceTimer)
})

// 监听路由变化
watch(() => route.params.id, () => {
  loadChallenge()
})
</script>

<style scoped lang="scss">
.challenge-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1e1e1e;

  &.is-loading {
    pointer-events: none;
    opacity: 0.7;
  }
}

// 顶部信息栏
.challenge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  background: #252526;
  border-bottom: 1px solid #333;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.challenge-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.challenge-title {
  font-size: 16px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0;
}

.challenge-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.difficulty-tag {
  border: none;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;

  .el-icon {
    font-size: 14px;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.best-result {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.best-label {
  font-size: 11px;
  color: #909399;
}

.best-stars {
  .star {
    font-size: 14px;
    color: #4a4a4a;

    &.filled {
      color: #f7ba2a;
    }
  }
}

// 主体区域
.challenge-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

// 侧边栏
.challenge-sidebar {
  display: flex;
  flex-direction: column;
  background: #252526;
  border-right: 1px solid #333;

  &.left {
    width: 40%;
    min-width: 350px;
    max-width: 500px;
  }

  &.right {
    width: 20%;
    min-width: 250px;
    max-width: 350px;
    border-right: none;
    border-left: 1px solid #333;
  }
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 12px;
  background: #2d2d30;
  border-bottom: 1px solid #333;
  font-size: 13px;
  color: #cccccc;

  .el-icon {
    font-size: 16px;
  }
}

.panel-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  color: #d4d4d4;
}

.panel-loading {
  flex: 1;
  padding: 20px;
}

// Markdown 样式
.markdown-body {
  font-size: 14px;
  line-height: 1.8;

  h1, h2, h3, h4 {
    color: #e0e0e0;
    margin-top: 20px;
    margin-bottom: 12px;
  }

  h2 {
    font-size: 18px;
    border-bottom: 1px solid #444;
    padding-bottom: 8px;
  }

  h3 {
    font-size: 16px;
  }

  p {
    margin-bottom: 12px;
  }

  ul, ol {
    padding-left: 20px;
    margin-bottom: 12px;
  }

  li {
    margin-bottom: 6px;
  }

  code {
    background: #3c3c3c;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', monospace;
    font-size: 13px;
    color: #dcdcaa;
  }

  pre {
    background: #1e1e1e;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    border: 1px solid #444;

    code {
      background: none;
      padding: 0;
    }
  }

  blockquote {
    border-left: 4px solid #409eff;
    padding-left: 12px;
    margin-left: 0;
    color: #909399;
  }
}

// 编辑器区域
.challenge-editor {
  display: flex;
  flex-direction: column;
  flex: 1;
  background: #1e1e1e;

  .panel-header {
    justify-content: space-between;
  }
}

.editor-actions {
  display: flex;
  gap: 8px;
}

.editor-container {
  flex: 1;
  position: relative;
}

// 预览区域
.preview-container {
  flex: 1;
  background: #fff;
}

.preview-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: #fff;
}

// 导师聊天
.mentor-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f7fa;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;

  &.user {
    flex-direction: row-reverse;

    .message-content {
      background: #409eff;
      color: #fff;
    }
  }
}

.message-avatar {
  font-size: 24px;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e4e7ed;
  background: #fff;

  .el-textarea {
    margin-bottom: 12px;
  }

  .el-button {
    width: 100%;
  }
}

// 响应式适配
@media (max-width: 1366px) {
  .challenge-sidebar {
    &.left {
      width: 35%;
      min-width: 300px;
    }

    &.right {
      width: 25%;
      min-width: 200px;
    }
  }

  .challenge-title {
    font-size: 14px;
  }

  .meta-item {
    font-size: 11px;
  }
}

@media (max-width: 1200px) {
  .challenge-sidebar {
    &.left {
      width: 30%;
      min-width: 280px;
    }

    &.right {
      display: none;
    }
  }
}
</style>

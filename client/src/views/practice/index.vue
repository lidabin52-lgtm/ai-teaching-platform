<template>
  <div class="practice-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>在线练习</h2>
      <p class="page-desc">自由选题，即时预览，AI辅助点评 — 巩固你的前端技能</p>
    </div>

    <!-- 分类标签 -->
    <div class="category-bar">
      <el-radio-group v-model="activeCategory" size="default">
        <el-radio-button label="all">全部题目</el-radio-button>
        <el-radio-button
          v-for="cat in practiceCategories"
          :key="cat.id"
          :label="cat.id"
        >
          {{ cat.icon }} {{ cat.name }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <!-- 题目选择区域 -->
    <div class="topic-section" v-if="!currentTopic">
      <el-row :gutter="16">
        <el-col
          :xs="24" :sm="12" :md="8" :lg="6"
          v-for="topic in filteredTopics"
          :key="topic.id"
        >
          <el-card
            class="topic-card"
            shadow="hover"
            @click="selectTopic(topic)"
          >
            <div class="topic-card-inner">
              <div class="topic-top">
                <el-tag :type="topic.difficultyType" size="small">{{ topic.difficulty }}</el-tag>
                <span class="topic-id">#{{ topic.id }}</span>
              </div>
              <h3 class="topic-title">{{ topic.title }}</h3>
              <p class="topic-desc">{{ topic.description }}</p>
              <div class="topic-footer">
                <el-tag size="small" effect="plain">{{ topic.language }}</el-tag>
                <span class="start-hint">点击开始练习 →</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 练习区域（选中题目后显示） -->
    <div class="practice-area" v-if="currentTopic">
      <!-- 返回按钮 + 题目信息 -->
      <div class="practice-header">
        <el-button text @click="backToList">
          <el-icon><ArrowLeft /></el-icon> 返回题库
        </el-button>
        <div class="topic-info">
          <h3>{{ currentTopic.title }}</h3>
          <div class="topic-meta">
            <el-tag :type="currentTopic.difficultyType" size="small">{{ currentTopic.difficulty }}</el-tag>
            <el-tag size="small" effect="plain">{{ currentTopic.language }}</el-tag>
            <el-tag size="small" effect="plain" type="info">{{ currentTopic.categoryId === 'html' ? 'HTML' : currentTopic.categoryId === 'css' ? 'CSS' : currentTopic.categoryId === 'js' ? 'JavaScript' : '综合' }}</el-tag>
          </div>
        </div>
        <div class="header-actions">
          <el-button size="small" @click="resetCode">
            <el-icon><RefreshRight /></el-icon> 重置代码
          </el-button>
          <el-button size="small" @click="showReference">
            <el-icon><View /></el-icon> 参考答案
          </el-button>
        </div>
      </div>

      <!-- 主体：三栏布局 -->
      <el-row :gutter="16" class="practice-body">
        <!-- 左栏：题目要求 -->
        <el-col :span="6">
          <el-card class="require-card">
            <template #header>
              <span>📋 题目要求</span>
            </template>
            <div class="require-content">
              <p class="topic-desc-full">{{ currentTopic.description }}</p>
              <h4>具体要求：</h4>
              <ul>
                <li v-for="(req, i) in currentTopic.requirements" :key="i">{{ req }}</li>
              </ul>
            </div>
          </el-card>
        </el-col>

        <!-- 中栏：代码编辑器 -->
        <el-col :span="12">
          <el-card class="editor-card">
            <template #header>
              <div class="editor-header">
                <span>💻 代码编辑器</span>
                <div class="editor-actions">
                  <el-button type="primary" size="small" @click="runCode" :loading="isRunning">
                    ▶ 运行预览
                  </el-button>
                  <el-button type="success" size="small" @click="submitCode" :loading="isSubmitting">
                    📤 提交代码
                  </el-button>
                </div>
              </div>
            </template>
            <CodeEditor
              ref="editorRef"
              v-model="code"
              :language="currentTopic.language"
              :file-name="currentTopic.fileName"
            />
          </el-card>
        </el-col>

        <!-- 右栏：运行结果 + AI点评 -->
        <el-col :span="6">
          <!-- 运行结果 -->
          <el-card class="preview-card" v-if="showPreview">
            <template #header>
              <span>🖥️ 运行结果</span>
            </template>
            <div class="preview-content">
              <iframe
                v-if="currentTopic.language === 'html'"
                :srcdoc="code"
                class="preview-iframe"
                sandbox="allow-scripts"
              ></iframe>
              <pre v-else class="console-output">{{ consoleOutput }}</pre>
            </div>
          </el-card>

          <!-- AI点评 -->
          <el-card class="review-card" :class="{ 'has-review': reviewResult }">
            <template #header>
              <span>🤖 AI点评</span>
            </template>
            <div class="review-content" v-if="reviewResult">
              <div class="review-score">
                <span class="score-label">代码评分</span>
                <span class="score-value" :class="scoreClass">{{ reviewResult.score }}</span>
              </div>
              <div class="review-items">
                <div
                  v-for="(item, i) in reviewResult.items"
                  :key="i"
                  class="review-item"
                  :class="item.type"
                >
                  <span class="review-icon">{{ item.type === 'pass' ? '✅' : item.type === 'warn' ? '⚠️' : '❌' }}</span>
                  <span>{{ item.text }}</span>
                </div>
              </div>
              <div class="review-suggestion" v-if="reviewResult.suggestion">
                <h4>💡 改进建议</h4>
                <p>{{ reviewResult.suggestion }}</p>
              </div>
            </div>
            <div class="review-empty" v-else>
              <p>点击「提交代码」获取AI点评</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 参考答案弹窗 -->
    <el-dialog v-model="referenceVisible" :title="'参考答案 - ' + (currentTopic ? currentTopic.title : '')" width="700px">
      <div class="reference-content">
        <el-alert type="info" :closable="false" show-icon style="margin-bottom: 16px">
          建议先自己完成练习，再查看参考答案
        </el-alert>
        <pre class="reference-code"><code>{{ currentTopic ? currentTopic.referenceCode : '' }}</code></pre>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, RefreshRight, View } from '@element-plus/icons-vue'
import CodeEditor from '@/components/CodeEditor.vue'
import { practiceCategories, practiceList } from './data.js'

// 分类筛选
const activeCategory = ref('all')
const filteredTopics = computed(() => {
  if (activeCategory.value === 'all') return practiceList
  return practiceList.filter(t => t.categoryId === activeCategory.value)
})

// 当前选中题目
const currentTopic = ref(null)
const code = ref('')
const editorRef = ref(null)

// 运行预览
const showPreview = ref(false)
const isRunning = ref(false)
const consoleOutput = ref('')

// AI点评
const isSubmitting = ref(false)
const reviewResult = ref(null)

// 参考答案
const referenceVisible = ref(false)

// 评分样式
const scoreClass = computed(() => {
  if (!reviewResult.value) return ''
  const s = reviewResult.value.score
  if (s >= 90) return 'score-excellent'
  if (s >= 70) return 'score-good'
  if (s >= 60) return 'score-pass'
  return 'score-fail'
})

// 选择题目
const selectTopic = (topic) => {
  currentTopic.value = topic
  code.value = topic.initialCode
  showPreview.value = false
  reviewResult.value = null
  consoleOutput.value = ''
}

// 返回列表
const backToList = () => {
  currentTopic.value = null
  showPreview.value = false
  reviewResult.value = null
  consoleOutput.value = ''
}

// 重置代码
const resetCode = () => {
  if (currentTopic.value) {
    code.value = currentTopic.value.initialCode
    showPreview.value = false
    reviewResult.value = null
    ElMessage.success('代码已重置')
  }
}

// 显示参考答案
const showReference = () => {
  referenceVisible.value = true
}

// 运行代码
const runCode = () => {
  if (!code.value.trim()) {
    ElMessage.warning('请先编写代码')
    return
  }
  isRunning.value = true
  showPreview.value = true

  if (currentTopic.value.language === 'html') {
    // HTML直接在iframe中预览
    setTimeout(() => {
      isRunning.value = false
    }, 500)
  } else {
    // JavaScript模拟console输出
    consoleOutput.value = ''
    const logs = []
    const mockConsole = {
      log: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')),
      error: (...args) => logs.push('ERROR: ' + args.join(' ')),
      warn: (...args) => logs.push('WARN: ' + args.join(' '))
    }

    try {
      const fn = new Function('console', code.value)
      fn(mockConsole)
      consoleOutput.value = logs.length > 0 ? logs.join('\n') : '(代码执行成功，无console输出)'
    } catch (e) {
      consoleOutput.value = '❌ 运行错误:\n' + e.message
    }
    isRunning.value = false
  }
}

// 提交代码 - 模拟AI点评
const submitCode = () => {
  if (!code.value.trim()) {
    ElMessage.warning('请先编写代码')
    return
  }

  isSubmitting.value = true

  // 模拟AI分析过程
  setTimeout(() => {
    const topic = currentTopic.value
    const userCode = code.value
    const items = []
    let score = 60

    // 基于代码内容进行简单分析
    const codeLen = userCode.length

    // 检查代码量
    if (codeLen > topic.initialCode.length * 0.5) {
      items.push({ type: 'pass', text: '代码结构完整，有实际编写内容' })
      score += 10
    } else {
      items.push({ type: 'fail', text: '代码内容过少，请补充实现' })
    }

    // 根据题目类型检查
    if (topic.categoryId === 'html') {
      if (userCode.includes('<!DOCTYPE')) {
        items.push({ type: 'pass', text: '包含DOCTYPE声明' })
        score += 5
      }
      if (userCode.includes('<meta')) {
        items.push({ type: 'pass', text: '设置了meta字符编码' })
        score += 5
      }
      if (userCode.includes('class="') || userCode.includes("class='")) {
        items.push({ type: 'pass', text: '使用了class类名，便于CSS样式控制' })
        score += 5
      }
      if (userCode.includes('<label')) {
        items.push({ type: 'pass', text: '表单使用了label标签，提升可访问性' })
        score += 5
      }
      if (userCode.includes('semantic') || userCode.includes('<header') || userCode.includes('<main') || userCode.includes('<section') || userCode.includes('<article')) {
        items.push({ type: 'pass', text: '使用了语义化标签，结构清晰' })
        score += 5
      }
    }

    if (topic.categoryId === 'css') {
      if (userCode.includes('display: flex') || userCode.includes('display:flex')) {
        items.push({ type: 'pass', text: '正确使用了Flex布局' })
        score += 10
      }
      if (userCode.includes('transition')) {
        items.push({ type: 'pass', text: '添加了过渡动画效果' })
        score += 5
      }
      if (userCode.includes('@media') || userCode.includes('media query')) {
        items.push({ type: 'pass', text: '考虑了响应式设计' })
        score += 5
      }
      if (userCode.includes('box-sizing: border-box') || userCode.includes('box-sizing:border-box')) {
        items.push({ type: 'pass', text: '使用了border-box盒模型（推荐实践）' })
        score += 3
      }
    }

    if (topic.categoryId === 'js' || topic.categoryId === 'comprehensive') {
      if (userCode.includes('function') || userCode.includes('=>') || userCode.includes('class ')) {
        items.push({ type: 'pass', text: '函数/类定义正确' })
        score += 5
      }
      if (userCode.includes('console.log')) {
        items.push({ type: 'pass', text: '包含测试代码，便于验证' })
        score += 3
      }
      if (userCode.includes('return')) {
        items.push({ type: 'pass', text: '函数有返回值' })
        score += 5
      }
      if (userCode.includes('//') || userCode.includes('/*') || userCode.includes('* @')) {
        items.push({ type: 'pass', text: '代码有注释，可读性好' })
        score += 5
      }
      if (userCode.includes('localStorage')) {
        items.push({ type: 'pass', text: '使用了localStorage进行数据持久化' })
        score += 5
      }
    }

    // 检查是否有明显问题
    if (userCode.includes('TODO') || userCode.includes('请补充') || userCode.includes('请在这里')) {
      items.push({ type: 'warn', text: '代码中包含未完成的部分（TODO/请补充）' })
      score -= 10
    }

    // 添加AI评审要点作为建议
    const suggestions = topic.aiReviewPoints || []
    const suggestion = suggestions.length > 0 ? suggestions[Math.floor(Math.random() * suggestions.length)] : '继续加油，尝试添加更多细节！'

    // 限制分数范围
    score = Math.max(30, Math.min(100, score))

    reviewResult.value = {
      score: score,
      items: items,
      suggestion: suggestion
    }

    isSubmitting.value = false

    if (score >= 80) {
      ElMessage.success('提交成功！代码质量不错，评分：' + score + '分')
    } else {
      ElMessage.info('提交成功！评分：' + score + '分，继续加油！')
    }
  }, 1500)
}
</script>

<style scoped lang="scss">
.practice-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;

  h2 {
    font-size: 24px;
    color: #303133;
    margin: 0 0 8px;
  }

  .page-desc {
    color: #909399;
    font-size: 14px;
    margin: 0;
  }
}

.category-bar {
  margin-bottom: 24px;
}

// ========== 题目卡片 ==========
.topic-section {
  .topic-card {
    margin-bottom: 16px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
    }
  }

  .topic-card-inner {
    .topic-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;

      .topic-id {
        color: #c0c4cc;
        font-size: 12px;
      }
    }

    .topic-title {
      font-size: 16px;
      color: #303133;
      margin: 0 0 8px;
    }

    .topic-desc {
      font-size: 13px;
      color: #909399;
      line-height: 1.5;
      margin: 0 0 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .topic-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .start-hint {
        font-size: 12px;
        color: #409eff;
      }
    }
  }
}

// ========== 练习区域 ==========
.practice-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;

  .topic-info {
    flex: 1;

    h3 {
      margin: 0 0 4px;
      font-size: 16px;
      color: #303133;
    }

    .topic-meta {
      display: flex;
      gap: 8px;
    }
  }

  .header-actions {
    display: flex;
    gap: 8px;
  }
}

.practice-body {
  .require-card {
    height: fit-content;
    max-height: 600px;
    overflow-y: auto;

    .require-content {
      h4 {
        margin: 16px 0 8px;
        color: #303133;
        font-size: 14px;
      }

      ul {
        padding-left: 18px;
        margin: 0;

        li {
          margin: 6px 0;
          font-size: 13px;
          color: #606266;
          line-height: 1.5;
        }
      }

      .topic-desc-full {
        color: #606266;
        line-height: 1.6;
        font-size: 14px;
        margin: 0;
      }
    }
  }

  .editor-card {
    .editor-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .editor-actions {
        display: flex;
        gap: 8px;
      }
    }
  }

  .preview-card {
    margin-bottom: 16px;

    .preview-content {
      .preview-iframe {
        width: 100%;
        height: 250px;
        border: 1px solid #e4e7ed;
        border-radius: 4px;
        background: white;
      }

      .console-output {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 12px;
        border-radius: 4px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        line-height: 1.5;
        max-height: 250px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-all;
        margin: 0;
      }
    }
  }

  .review-card {
    min-height: 200px;

    .review-content {
      .review-score {
        text-align: center;
        margin-bottom: 16px;
        padding: 12px;
        background: #f5f7fa;
        border-radius: 8px;

        .score-label {
          display: block;
          font-size: 12px;
          color: #909399;
          margin-bottom: 4px;
        }

        .score-value {
          font-size: 36px;
          font-weight: bold;

          &.score-excellent { color: #67c23a; }
          &.score-good { color: #409eff; }
          &.score-pass { color: #e6a23c; }
          &.score-fail { color: #f56c6c; }
        }
      }

      .review-items {
        .review-item {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          padding: 6px 0;
          font-size: 13px;
          line-height: 1.5;

          .review-icon {
            flex-shrink: 0;
          }

          &.warn { color: #e6a23c; }
          &.fail { color: #f56c6c; }
          &.pass { color: #67c23a; }
        }
      }

      .review-suggestion {
        margin-top: 12px;
        padding: 12px;
        background: #ecf5ff;
        border-radius: 6px;

        h4 {
          margin: 0 0 6px;
          font-size: 13px;
          color: #409eff;
        }

        p {
          margin: 0;
          font-size: 13px;
          color: #606266;
          line-height: 1.5;
        }
      }
    }

    .review-empty {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 150px;
      color: #c0c4cc;
      font-size: 14px;
    }
  }
}

// ========== 参考答案弹窗 ==========
.reference-content {
  .reference-code {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 16px;
    border-radius: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    line-height: 1.6;
    overflow-x: auto;
    max-height: 500px;
    overflow-y: auto;
    margin: 0;
  }
}
</style>

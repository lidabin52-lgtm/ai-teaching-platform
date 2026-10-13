<template>
  <div class="course-detail-page">
    <!-- 返回按钮 -->
    <div class="back-bar">
      <el-button text @click="$router.push('/course')">
        <el-icon><ArrowLeft /></el-icon> 返回课程中心
      </el-button>
    </div>

    <!-- 课程标题 -->
    <el-card class="course-header">
      <div class="header-content">
        <span class="course-icon">{{ course.icon }}</span>
        <div class="header-info">
          <h1>{{ course.title }}</h1>
          <div class="header-meta">
            <el-tag :type="course.tagType" size="small">{{ course.difficulty }}</el-tag>
            <span>🎮 {{ course.challenges }} 个闯关关卡</span>
            <span>📖 {{ course.sections.length }} 个知识章节</span>
          </div>
        </div>
        <el-button type="primary" size="large" @click="goToChallenge">
          开始闯关 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
    </el-card>

    <!-- 章节列表 -->
    <div class="sections">
      <el-card v-for="(section, index) in course.sections" :key="index" class="section-card">
        <template #header>
          <div class="section-title">
            <el-tag type="primary" size="small">第{{ index + 1 }}章</el-tag>
            <h3>{{ section.title }}</h3>
          </div>
        </template>

        <div class="section-content">
          <!-- 知识点讲解 -->
          <div class="knowledge-text" v-html="renderMarkdown(section.content)"></div>

          <!-- 代码示例 -->
          <div v-if="section.codeExample" class="code-example">
            <div class="code-header">
              <span>{{ section.codeTitle || '代码示例' }}</span>
              <el-button text size="small" @click="copyCode(section.codeExample)">复制代码</el-button>
            </div>
            <pre class="code-block"><code>{{ section.codeExample }}</code></pre>
          </div>

          <!-- 要点总结 -->
          <div v-if="section.keyPoints" class="key-points">
            <h4>💡 要点总结</h4>
            <ul>
              <li v-for="(point, i) in section.keyPoints" :key="i">{{ point }}</li>
            </ul>
          </div>

          <!-- 课后练习提示 -->
          <div v-if="section.practiceTip" class="practice-tip">
            <h4>🎯 动手练习</h4>
            <p>{{ section.practiceTip }}</p>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 底部：开始闯关 -->
    <div class="bottom-action">
      <el-button type="primary" size="large" @click="goToChallenge">
        🚀 学完了，去闯关吧！
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import { coursesList } from '@/data/courses.js'

const route = useRoute()
const router = useRouter()

// 当前课程
const courseId = computed(() => parseInt(route.params.id))
const course = computed(() => {
  const found = coursesList.find(c => c.id === courseId.value)
  return found || coursesList[0]
})

// 渲染Markdown
const renderMarkdown = (text) => {
  if (!text) return ''
  try {
    return marked(text)
  } catch {
    return text
  }
}

// 复制代码
const copyCode = async (code) => {
  try {
    await navigator.clipboard.writeText(code)
    ElMessage.success('代码已复制')
  } catch {
    ElMessage.error('复制失败')
  }
}

// 跳转到闯关
const goToChallenge = () => {
  if (course.value.startChallengeId) {
    router.push(`/challenge/${course.value.startChallengeId}`)
  } else {
    router.push('/challenge')
  }
}
</script>

<style scoped lang="scss">
.course-detail-page {
  max-width: 900px;
  margin: 0 auto;
}

.back-bar {
  margin-bottom: 16px;
}

.course-header {
  margin-bottom: 24px;

  .header-content {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .course-icon {
    font-size: 56px;
  }

  .header-info {
    flex: 1;

    h1 {
      margin: 0 0 8px;
      font-size: 24px;
      color: #303133;
    }

    .header-meta {
      display: flex;
      align-items: center;
      gap: 16px;
      color: #909399;
      font-size: 14px;
    }
  }
}

.section-card {
  margin-bottom: 20px;

  .section-title {
    display: flex;
    align-items: center;
    gap: 12px;

    h3 {
      margin: 0;
      font-size: 18px;
      color: #303133;
    }
  }
}

.section-content {
  .knowledge-text {
    line-height: 1.8;
    color: #303133;

    :deep(h2) {
      font-size: 20px;
      margin: 20px 0 12px;
      padding-bottom: 8px;
      border-bottom: 2px solid #409eff;
    }

    :deep(h3) {
      font-size: 16px;
      margin: 16px 0 8px;
    }

    :deep(p) {
      margin: 8px 0;
    }

    :deep(ul), :deep(ol) {
      padding-left: 20px;
      margin: 8px 0;
    }

    :deep(li) {
      margin: 4px 0;
    }

    :deep(code) {
      background: #f5f7fa;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 14px;
      color: #e6a23c;
    }

    :deep(strong) {
      color: #303133;
    }
  }

  .code-example {
    margin: 16px 0;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #e4e7ed;

    .code-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 16px;
      background: #f5f7fa;
      font-size: 13px;
      color: #606266;
    }

    .code-block {
      margin: 0;
      padding: 16px;
      background: #1e1e1e;
      color: #d4d4d4;
      font-family: 'Consolas', 'Monaco', monospace;
      font-size: 14px;
      line-height: 1.6;
      overflow-x: auto;
    }
  }

  .key-points {
    margin: 16px 0;
    padding: 16px;
    background: #ecf5ff;
    border-radius: 8px;

    h4 {
      margin: 0 0 12px;
      color: #409eff;
    }

    ul {
      margin: 0;
      padding-left: 20px;

      li {
        margin: 6px 0;
        line-height: 1.6;
        color: #303133;
      }
    }
  }

  .practice-tip {
    margin: 16px 0;
    padding: 16px;
    background: #fdf6ec;
    border-radius: 8px;

    h4 {
      margin: 0 0 8px;
      color: #e6a23c;
    }

    p {
      margin: 0;
      color: #606266;
      line-height: 1.6;
    }
  }
}

.bottom-action {
  text-align: center;
  padding: 40px 0;
}
</style>

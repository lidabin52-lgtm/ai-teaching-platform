<template>
  <div class="course-page">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="page-header">
          <h2>📚 课程中心</h2>
          <p>系统学习前端开发技能，点击课程即可进入对应闯关练习</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="course-list">
      <el-col :span="8" v-for="course in courses" :key="course.id">
        <el-card class="course-card" shadow="hover" @click="goToCourse(course)">
          <div class="course-icon">{{ course.icon }}</div>
          <h3>{{ course.title }}</h3>
          <p>{{ course.description }}</p>
          <div class="course-meta">
            <span>🎮 {{ course.challenges }} 个关卡</span>
            <span>📊 {{ course.difficulty }}</span>
          </div>
          <el-progress
            :percentage="course.progress"
            :stroke-width="8"
            :color="course.progressColor"
          />
          <div class="course-action">
            <el-button type="primary" text>
              {{ course.progress > 0 ? '继续学习' : '开始闯关' }}
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

// 课程与关卡的映射关系
const courses = ref([
  {
    id: 1,
    icon: '🌐',
    title: 'HTML基础',
    description: '学习HTML标签、语义化、表单等基础知识',
    challenges: 5,
    difficulty: '青铜段位',
    progress: 0,
    progressColor: '#CD7F32',
    // 对应闯关关卡的起始ID
    startChallengeId: 1,
    tier: 'bronze',
  },
  {
    id: 2,
    icon: '🎨',
    title: 'CSS样式',
    description: '掌握CSS选择器、布局、定位等核心技能',
    challenges: 4,
    difficulty: '白银段位',
    progress: 0,
    progressColor: '#C0C0C0',
    startChallengeId: 6,
    tier: 'silver',
  },
  {
    id: 3,
    icon: '⚡',
    title: 'JavaScript基础',
    description: '学习JS语法、DOM操作、事件处理等',
    challenges: 3,
    difficulty: '黄金段位',
    progress: 0,
    progressColor: '#FFD700',
    startChallengeId: 10,
    tier: 'gold',
  },
  {
    id: 4,
    icon: '💎',
    title: '综合应用',
    description: '综合运用HTML/CSS/JS完成实际项目',
    challenges: 2,
    difficulty: '钻石段位',
    progress: 0,
    progressColor: '#B9F2FF',
    startChallengeId: 13,
    tier: 'diamond',
  },
  {
    id: 5,
    icon: '👑',
    title: '王者挑战',
    description: '终极挑战：独立完成个人作品集网站',
    challenges: 1,
    difficulty: '王者段位',
    progress: 0,
    progressColor: '#FF6B6B',
    startChallengeId: 15,
    tier: 'king',
  },
  {
    id: 6,
    icon: '🤖',
    title: 'AI辅助学习',
    description: 'AI导师全程陪伴，智能答疑与代码指导',
    challenges: 0,
    difficulty: '全段位',
    progress: 0,
    progressColor: '#409eff',
    startChallengeId: 0,
    tier: 'ai',
  },
])

// 点击课程 → 跳转到课程详情页
const goToCourse = (course) => {
  router.push(`/course/${course.id}`)
}
</script>

<style scoped lang="scss">
.course-page {
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    margin-bottom: 24px;
    text-align: center;

    h2 {
      margin: 0 0 10px;
      color: #409eff;
      font-size: 24px;
    }

    p {
      margin: 0;
      color: #909399;
      font-size: 14px;
    }
  }

  .course-card {
    margin-bottom: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    border-radius: 12px;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }

    .course-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    h3 {
      margin: 0 0 8px;
      color: #303133;
      font-size: 18px;
    }

    p {
      margin: 0 0 16px;
      color: #909399;
      font-size: 13px;
      line-height: 1.5;
    }

    .course-meta {
      display: flex;
      justify-content: space-around;
      margin-bottom: 12px;
      font-size: 13px;
      color: #606266;
    }

    .course-action {
      margin-top: 12px;
    }
  }
}
</style>

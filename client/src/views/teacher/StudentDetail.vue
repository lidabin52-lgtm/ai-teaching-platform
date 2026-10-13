<template>
  <!-- 学生个体详情页 -->
  <div class="student-detail">
    <!-- 顶部导航 -->
    <div class="detail-header">
      <el-button text @click="$router.push('/teacher')">
        <el-icon><ArrowLeft /></el-icon>
        返回仪表盘
      </el-button>
      <h2>学生详情</h2>
    </div>

    <div class="detail-content">
      <!-- 左侧：学生信息 + 雷达图 -->
      <div class="detail-left">
        <!-- 学生基本信息卡片 -->
        <div class="info-card">
          <div class="info-avatar">
            <el-avatar :size="72" class="avatar-large">
              {{ studentInfo.nickname?.charAt(0) || '?' }}
            </el-avatar>
            <el-tag
              :type="studentInfo.status === 'active' ? 'success' : 'info'"
              size="small"
              class="status-tag"
            >
              {{ studentInfo.status === 'active' ? '活跃' : '不活跃' }}
            </el-tag>
          </div>
          <div class="info-fields">
            <div class="field-item">
              <span class="field-label">姓名</span>
              <span class="field-value">{{ studentInfo.nickname }}</span>
            </div>
            <div class="field-item">
              <span class="field-label">邮箱</span>
              <span class="field-value">{{ studentInfo.email }}</span>
            </div>
            <div class="field-item">
              <span class="field-label">注册时间</span>
              <span class="field-value">{{ studentInfo.createdAt }}</span>
            </div>
            <div class="field-item">
              <span class="field-label">最后活跃</span>
              <span class="field-value">{{ studentInfo.lastActive }}</span>
            </div>
          </div>
          <div class="info-stats">
            <div class="mini-stat">
              <span class="mini-value">{{ studentInfo.completed }}</span>
              <span class="mini-label">已通关</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value stars">⭐ {{ studentInfo.totalStars }}</span>
              <span class="mini-label">总星数</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value">{{ studentInfo.avgScore }}</span>
              <span class="mini-label">平均分</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value">{{ studentInfo.currentStreak }}天</span>
              <span class="mini-label">连续打卡</span>
            </div>
          </div>
        </div>

        <!-- 能力雷达图 -->
        <div class="radar-card">
          <h3>能力雷达图</h3>
          <div ref="radarRef" class="radar-container"></div>
        </div>

        <!-- 学习预警 -->
        <div class="warning-card">
          <h3>
            <el-icon><Warning /></el-icon>
            学习预警
          </h3>
          <div class="warning-list">
            <div
              v-for="w in warnings"
              :key="w.type"
              :class="['warning-item', w.level]"
            >
              <el-icon><component :is="w.icon" /></el-icon>
              <div class="warning-text">
                <span class="warning-title">{{ w.title }}</span>
                <span class="warning-desc">{{ w.desc }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：闯关时间线 -->
      <div class="detail-right">
        <div class="timeline-card">
          <div class="timeline-header">
            <h3>闯关时间线</h3>
            <el-radio-group v-model="timelineFilter" size="small">
              <el-radio-button value="all">全部</el-radio-button>
              <el-radio-button value="completed">已通关</el-radio-button>
              <el-radio-button value="stuck">卡关中</el-radio-button>
            </el-radio-group>
          </div>

          <div class="timeline-list">
            <div
              v-for="item in filteredTimeline"
              :key="item.id"
              :class="['timeline-item', item.status]"
            >
              <!-- 时间线节点 -->
              <div class="timeline-node">
                <div class="node-dot" :style="{ borderColor: getDifficultyColor(item.difficulty) }">
                  <span v-if="item.status === 'completed'" class="node-check">✓</span>
                  <span v-else class="node-lock">🔒</span>
                </div>
                <div class="node-line"></div>
              </div>

              <!-- 内容 -->
              <div class="timeline-content">
                <div class="content-header">
                  <span class="challenge-title">{{ item.title }}</span>
                  <div class="content-tags">
                    <el-tag
                      size="small"
                      :color="getDifficultyColor(item.difficulty)"
                      effect="dark"
                      style="border: none"
                    >
                      {{ getDifficultyLabel(item.difficulty) }}
                    </el-tag>
                    <el-tag
                      size="small"
                      :type="item.status === 'completed' ? 'success' : 'warning'"
                    >
                      {{ item.status === 'completed' ? '已通关' : '卡关中' }}
                    </el-tag>
                  </div>
                </div>

                <div class="content-body">
                  <!-- 星数 -->
                  <div v-if="item.status === 'completed'" class="result-stars">
                    <span
                      v-for="n in 3"
                      :key="n"
                      class="star"
                      :class="{ filled: n <= item.stars }"
                    >★</span>
                    <span class="score-text">{{ item.score }}分</span>
                  </div>

                  <!-- AI评语摘要 -->
                  <div v-if="item.aiSummary" class="ai-summary">
                    <el-icon><ChatDot-Square /></el-icon>
                    <span>{{ item.aiSummary }}</span>
                  </div>

                  <!-- 尝试次数 -->
                  <div class="attempt-info">
                    <el-icon><Edit /></el-icon>
                    <span>尝试 {{ item.attempts }} 次</span>
                    <span class="time-info">{{ item.completedAt }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import {
  ArrowLeft, Warning, ChatDotSquare, Edit,
  Clock, TrendCharts, Opportunity
} from '@element-plus/icons-vue'

const route = useRoute()
const timelineFilter = ref('all')
const radarRef = ref(null)
let radarChart = null

// ========== Mock数据 ==========
const studentInfo = ref({
  id: 1,
  nickname: '张三',
  email: 'zhangsan@example.com',
  createdAt: '2024-09-01',
  lastActive: '10分钟前',
  status: 'active',
  completed: 12,
  totalStars: 28,
  avgScore: 85,
  currentStreak: 5
})

const warnings = ref([
  {
    type: 'stuck',
    level: 'danger',
    icon: 'Warning',
    title: 'JavaScript闭包关卡卡关超过3天',
    desc: '已尝试4次仍未通过，建议关注并提供指导'
  },
  {
    type: 'decline',
    level: 'warning',
    icon: 'TrendCharts',
    title: '近期平均分呈下降趋势',
    desc: '近5次提交平均分72，低于历史平均85分'
  },
  {
    type: 'inactive',
    level: 'info',
    icon: 'Clock',
    title: '本周活跃度降低',
    desc: '本周仅登录2次，低于班级平均4.5次'
  }
])

const timeline = ref([
  {
    id: 12, title: 'Vue 3组合式API', difficulty: 'diamond', status: 'stuck',
    attempts: 4, stars: 0, score: 0, aiSummary: '', completedAt: '进行中'
  },
  {
    id: 11, title: 'Promise与异步编程', difficulty: 'gold', status: 'completed',
    attempts: 3, stars: 2, score: 78,
    aiSummary: '异步流程理解到位，建议加强错误处理练习。',
    completedAt: '2天前'
  },
  {
    id: 10, title: 'ES6+新特性', difficulty: 'gold', status: 'completed',
    attempts: 2, stars: 3, score: 92,
    aiSummary: '对新特性掌握扎实，代码简洁优雅。',
    completedAt: '3天前'
  },
  {
    id: 8, title: 'CSS Grid复杂布局', difficulty: 'gold', status: 'completed',
    attempts: 4, stars: 2, score: 75,
    aiSummary: 'Grid布局基本掌握，复杂嵌套场景需加强。',
    completedAt: '5天前'
  },
  {
    id: 7, title: 'Flex布局进阶', difficulty: 'silver', status: 'completed',
    attempts: 2, stars: 3, score: 88,
    aiSummary: 'Flex布局运用熟练，代码规范性好。',
    completedAt: '1周前'
  },
  {
    id: 5, title: 'JavaScript DOM操作', difficulty: 'silver', status: 'completed',
    attempts: 3, stars: 2, score: 80,
    aiSummary: 'DOM操作基础扎实，事件处理可更优化。',
    completedAt: '1周前'
  },
  {
    id: 3, title: 'Flex布局：创建响应式卡片', difficulty: 'bronze', status: 'completed',
    attempts: 1, stars: 3, score: 95,
    aiSummary: '完美完成！Flex属性运用准确，响应式处理到位。',
    completedAt: '2周前'
  },
  {
    id: 2, title: 'CSS选择器：美化个人主页', difficulty: 'bronze', status: 'completed',
    attempts: 1, stars: 3, score: 90,
    aiSummary: '选择器使用正确，样式效果美观。',
    completedAt: '2周前'
  },
  {
    id: 1, title: 'HTML基础：创建第一个网页', difficulty: 'bronze', status: 'completed',
    attempts: 1, stars: 3, score: 98,
    aiSummary: 'HTML结构完整规范，文档格式正确。',
    completedAt: '2周前'
  }
])

const filteredTimeline = computed(() => {
  if (timelineFilter.value === 'all') return timeline.value
  return timeline.value.filter(item => item.status === timelineFilter.value)
})

// ========== ECharts ==========
const initRadar = () => {
  if (!radarRef.value) return
  radarChart = echarts.init(radarRef.value)

  radarChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: [
        { name: 'HTML', max: 100 },
        { name: 'CSS', max: 100 },
        { name: 'JavaScript', max: 100 },
        { name: '响应式', max: 100 },
        { name: '调试能力', max: 100 },
        { name: '代码规范', max: 100 }
      ],
      shape: 'circle',
      splitNumber: 5,
      axisName: {
        color: '#606266',
        fontSize: 12
      },
      splitArea: {
        areaStyle: {
          color: ['#fff', '#F5F7FA', '#fff', '#F5F7FA', '#fff']
        }
      },
      axisLine: { lineStyle: { color: '#DCDFE6' } },
      splitLine: { lineStyle: { color: '#EBEEF5' } }
    },
    series: [{
      type: 'radar',
      data: [
        {
          value: [95, 88, 75, 70, 65, 85],
          name: '能力值',
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.2)'
          },
          lineStyle: {
            color: '#409EFF',
            width: 2
          },
          itemStyle: {
            color: '#409EFF'
          }
        },
        {
          value: [80, 75, 60, 55, 50, 70],
          name: '班级平均',
          areaStyle: {
            color: 'rgba(144, 147, 153, 0.1)'
          },
          lineStyle: {
            color: '#909399',
            width: 1,
            type: 'dashed'
          },
          itemStyle: {
            color: '#909399'
          }
        }
      ]
    }],
    legend: {
      data: ['能力值', '班级平均'],
      bottom: 0,
      textStyle: { color: '#606266' }
    }
  })
}

// ========== 工具方法 ==========
const getDifficultyColor = (d) => {
  const colors = { bronze: '#CD7F32', silver: '#C0C0C0', gold: '#FFD700', diamond: '#B9F2FF', king: '#FF6B6B' }
  return colors[d] || '#999'
}

const getDifficultyLabel = (d) => {
  const labels = { bronze: '青铜', silver: '白银', gold: '黄金', diamond: '钻石', king: '王者' }
  return labels[d] || d
}

// ========== 生命周期 ==========
onMounted(() => {
  nextTick(() => {
    initRadar()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  radarChart?.dispose()
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  radarChart?.resize()
}
</script>

<style scoped lang="scss">
.student-detail {
  min-height: 100vh;
  background: #F0F2F5;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #EBEEF5;

  h2 {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }
}

.detail-content {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 20px;
  padding: 20px 24px;
}

// 左侧
.detail-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.info-avatar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.avatar-large {
  background: linear-gradient(135deg, #409EFF, #337ECC);
  color: #fff;
  font-size: 28px;
}

.status-tag {
  position: relative;
  top: 20px;
}

.info-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #EBEEF5;
}

.field-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  font-size: 13px;
  color: #909399;
}

.field-value {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.info-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.mini-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  background: #F5F7FA;
  border-radius: 8px;
}

.mini-value {
  font-size: 20px;
  font-weight: 700;
  color: #303133;

  &.stars {
    color: #E6A23C;
    font-size: 16px;
  }
}

.mini-label {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

// 雷达图
.radar-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);

  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 12px 0;
  }
}

.radar-container {
  height: 300px;
}

// 学习预警
.warning-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);

  h3 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 16px 0;

    .el-icon { color: #E6A23C; }
  }
}

.warning-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.warning-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid;

  &.danger {
    background: #FEF0F0;
    border-color: #F56C6C;
    .el-icon { color: #F56C6C; }
  }

  &.warning {
    background: #FDF6EC;
    border-color: #E6A23C;
    .el-icon { color: #E6A23C; }
  }

  &.info {
    background: #ECF5FF;
    border-color: #409EFF;
    .el-icon { color: #409EFF; }
  }
}

.warning-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.warning-title {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
}

.warning-desc {
  font-size: 12px;
  color: #909399;
}

// 右侧时间线
.detail-right {
  min-width: 0;
}

.timeline-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }
}

.timeline-list {
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 20px;
  position: relative;
  padding-bottom: 24px;

  &:last-child .node-line {
    display: none;
  }
}

.timeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.node-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 3px solid;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  z-index: 1;

  .node-check {
    color: #67C23A;
    font-weight: bold;
  }
}

.node-line {
  width: 2px;
  flex: 1;
  background: #EBEEF5;
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
  background: #FAFAFA;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #EBEEF5;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.challenge-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.content-tags {
  display: flex;
  gap: 6px;
}

.content-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.result-stars {
  display: flex;
  align-items: center;
  gap: 4px;

  .star {
    font-size: 18px;
    color: #DCDFE6;

    &.filled {
      color: #F7BA2A;
    }
  }

  .score-text {
    margin-left: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #409EFF;
  }
}

.ai-summary {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 10px 12px;
  background: #F5F7FA;
  border-radius: 6px;
  border-left: 3px solid #409EFF;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;

  .el-icon {
    color: #409EFF;
    margin-top: 2px;
    flex-shrink: 0;
  }
}

.attempt-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;

  .el-icon { font-size: 14px; }

  .time-info {
    margin-left: auto;
  }
}

// 响应式
@media (max-width: 1366px) {
  .detail-content {
    grid-template-columns: 340px 1fr;
    gap: 16px;
    padding: 16px;
  }
}

@media (max-width: 1024px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
}
</style>

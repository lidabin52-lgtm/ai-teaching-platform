<template>
  <!-- 教师学情仪表盘 -->
  <div class="teacher-dashboard">
    <!-- 左侧导航 -->
    <aside class="dashboard-sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">📊</span>
        <span class="logo-text">学情分析</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        @select="handleMenuSelect"
        class="sidebar-menu"
      >
        <el-menu-item index="overview">
          <el-icon><DataAnalysis /></el-icon>
          <span>班级概览</span>
        </el-menu-item>
        <el-menu-item index="students">
          <el-icon><User /></el-icon>
          <span>学生列表</span>
        </el-menu-item>
        <el-menu-item index="challenges">
          <el-icon><Trophy /></el-icon>
          <span>关卡分析</span>
        </el-menu-item>
        <el-menu-item index="errors">
          <el-icon><Warning /></el-icon>
          <span>高频错误</span>
        </el-menu-item>
      </el-menu>
      <div class="sidebar-footer">
        <el-button type="info" text @click="$router.push('/')">
          <el-icon><Back /></el-icon>
          返回首页
        </el-button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="dashboard-main">
      <!-- 顶部统计卡片 -->
      <div class="stats-row">
        <div class="stat-card" v-for="stat in statsCards" :key="stat.label">
          <div class="stat-icon" :style="{ backgroundColor: stat.bgColor }">
            <el-icon :size="24" :style="{ color: stat.color }">
              <component :is="stat.icon" />
            </el-icon>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
          <div class="stat-trend" :class="stat.trend">
            {{ stat.trendValue }}
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-row">
        <!-- 左上：知识掌握热力图 -->
        <div class="chart-card heatmap-card">
          <div class="chart-header">
            <h3>知识掌握热力图</h3>
            <el-select v-model="selectedClass" size="small" style="width: 140px">
              <el-option label="全部班级" value="all" />
              <el-option label="前端一班" value="class1" />
              <el-option label="前端二班" value="class2" />
            </el-select>
          </div>
          <div ref="heatmapRef" class="chart-container"></div>
        </div>

        <!-- 右上：高频错误饼图 -->
        <div class="chart-card error-card">
          <div class="chart-header">
            <h3>高频错误分布</h3>
            <el-tag size="small" type="info">AI聚类分析</el-tag>
          </div>
          <div ref="errorPieRef" class="chart-container"></div>
        </div>
      </div>

      <!-- 下方：卡关排行榜 -->
      <div class="chart-card table-card">
        <div class="chart-header">
          <h3>卡关排行榜</h3>
          <el-button type="primary" size="small" plain>
            <el-icon><Download /></el-icon>
            导出报告
          </el-button>
        </div>
        <el-table :data="stuckChallenges" stripe style="width: 100%">
          <el-table-column type="index" label="#" width="50" />
          <el-table-column prop="title" label="关卡名称" min-width="200">
            <template #default="{ row }">
              <div class="challenge-name">
                <el-tag
                  size="small"
                  :color="getDifficultyColor(row.difficulty)"
                  effect="dark"
                  style="border: none; margin-right: 8px"
                >
                  {{ getDifficultyLabel(row.difficulty) }}
                </el-tag>
                {{ row.title }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="100" />
          <el-table-column prop="totalStudents" label="参与人数" width="100" />
          <el-table-column prop="stuckCount" label="卡关人数" width="100">
            <template #default="{ row }">
              <span class="stuck-count" :class="{ high: row.stuckRate > 60 }">
                {{ row.stuckCount }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="stuckRate" label="卡关率" width="120">
            <template #default="{ row }">
              <div class="rate-cell">
                <el-progress
                  :percentage="row.stuckRate"
                  :color="getRateColor(row.stuckRate)"
                  :stroke-width="8"
                  :show-text="true"
                />
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="avgAttempts" label="平均尝试次数" width="120" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" text size="small" @click="viewDetail(row)">
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 学生列表（简化版） -->
      <div class="chart-card student-list-card">
        <div class="chart-header">
          <h3>学生列表</h3>
          <el-input
            v-model="searchStudent"
            placeholder="搜索学生..."
            size="small"
            style="width: 200px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <el-table
          :data="filteredStudents"
          stripe
          style="width: 100%"
          @row-click="viewStudent"
          highlight-current-row
          cursor-pointer
        >
          <el-table-column prop="nickname" label="学生" min-width="120">
            <template #default="{ row }">
              <div class="student-name">
                <el-avatar :size="28" class="student-avatar">
                  {{ row.nickname?.charAt(0) || '?' }}
                </el-avatar>
                {{ row.nickname }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="completed" label="已通关" width="80" />
          <el-table-column prop="totalStars" label="总星数" width="80">
            <template #default="{ row }">
              <span class="stars-text">⭐ {{ row.totalStars }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="avgScore" label="平均分" width="80" />
          <el-table-column prop="lastActive" label="最后活跃" width="120" />
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
                {{ row.status === 'active' ? '活跃' : '不活跃' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import {
  DataAnalysis, User, Trophy, Warning, Back, Download, Search
} from '@element-plus/icons-vue'

const router = useRouter()
const activeMenu = ref('overview')
const selectedClass = ref('all')
const searchStudent = ref('')

// ========== Mock数据 ==========

const statsCards = ref([
  { label: '班级总人数', value: 48, icon: 'User', color: '#409EFF', bgColor: '#ECF5FF', trend: 'up', trendValue: '+3' },
  { label: '已激活学生', value: 42, icon: 'UserFilled', color: '#67C23A', bgColor: '#F0F9EB', trend: 'up', trendValue: '+5' },
  { label: '整体通关率', value: '68.5%', icon: 'Trophy', color: '#E6A23C', bgColor: '#FDF6EC', trend: 'up', trendValue: '+2.3%' },
  { label: '平均星数', value: '2.3', icon: 'Star', color: '#F56C6C', bgColor: '#FEF0F0', trend: 'down', trendValue: '-0.1' }
])

const stuckChallenges = ref([
  { id: 5, title: 'JavaScript闭包与作用域', difficulty: 'silver', category: 'JavaScript', totalStudents: 42, stuckCount: 28, stuckRate: 67, avgAttempts: 3.5 },
  { id: 8, title: 'CSS Grid复杂布局', difficulty: 'gold', category: 'CSS', totalStudents: 35, stuckCount: 22, stuckRate: 63, avgAttempts: 4.1 },
  { id: 3, title: 'Flex布局：创建响应式卡片', difficulty: 'bronze', category: 'CSS', totalStudents: 48, stuckCount: 15, stuckRate: 31, avgAttempts: 2.2 },
  { id: 12, title: 'Vue 3组合式API', difficulty: 'diamond', category: 'Vue', totalStudents: 20, stuckCount: 14, stuckRate: 70, avgAttempts: 4.8 },
  { id: 7, title: 'Promise与异步编程', difficulty: 'gold', category: 'JavaScript', totalStudents: 30, stuckCount: 18, stuckRate: 60, avgAttempts: 3.8 },
  { id: 2, title: 'CSS选择器：美化个人主页', difficulty: 'bronze', category: 'CSS', totalStudents: 48, stuckCount: 8, stuckRate: 17, avgAttempts: 1.5 }
])

const students = ref([
  { id: 1, nickname: '张三', completed: 12, totalStars: 28, avgScore: 85, lastActive: '10分钟前', status: 'active' },
  { id: 2, nickname: '李四', completed: 10, totalStars: 22, avgScore: 78, lastActive: '1小时前', status: 'active' },
  { id: 3, nickname: '王五', completed: 8, totalStars: 18, avgScore: 72, lastActive: '3小时前', status: 'active' },
  { id: 4, nickname: '赵六', completed: 15, totalStars: 35, avgScore: 91, lastActive: '30分钟前', status: 'active' },
  { id: 5, nickname: '孙七', completed: 5, totalStars: 10, avgScore: 65, lastActive: '2天前', status: 'inactive' },
  { id: 6, nickname: '周八', completed: 11, totalStars: 25, avgScore: 80, lastActive: '5小时前', status: 'active' },
  { id: 7, nickname: '吴九', completed: 3, totalStars: 6, avgScore: 58, lastActive: '5天前', status: 'inactive' },
  { id: 8, nickname: '郑十', completed: 9, totalStars: 20, avgScore: 76, lastActive: '昨天', status: 'active' }
])

const filteredStudents = computed(() => {
  if (!searchStudent.value) return students.value
  const keyword = searchStudent.value.toLowerCase()
  return students.value.filter(s => s.nickname.toLowerCase().includes(keyword))
})

// ========== ECharts ==========
const heatmapRef = ref(null)
const errorPieRef = ref(null)
let heatmapChart = null
let errorPieChart = null

const initHeatmap = () => {
  if (!heatmapRef.value) return
  heatmapChart = echarts.init(heatmapRef.value)

  const categories = ['HTML', 'CSS', 'JavaScript', 'Vue', 'React']
  const difficulties = ['青铜', '白银', '黄金', '钻石', '王者']

  // 生成热力图数据 [categoryIndex, difficultyIndex, value]
  const data = [
    [0, 0, 92], [0, 1, 75], [0, 2, 45], [0, 3, 20], [0, 4, 5],
    [1, 0, 85], [1, 1, 68], [1, 2, 40], [1, 3, 15], [1, 4, 3],
    [2, 0, 78], [2, 1, 55], [2, 2, 30], [2, 3, 10], [2, 4, 2],
    [3, 0, 60], [3, 1, 40], [3, 2, 20], [3, 3, 8], [3, 4, 1],
    [4, 0, 50], [4, 1, 30], [4, 2, 15], [4, 3, 5], [4, 4, 0]
  ]

  heatmapChart.setOption({
    tooltip: {
      position: 'top',
      formatter: (params) => `${categories[params.value[0]]} - ${difficulties[params.value[1]]}<br/>掌握率: ${params.value[2]}%`
    },
    grid: { top: 10, bottom: 60, left: 80, right: 30 },
    xAxis: {
      type: 'category',
      data: categories,
      splitArea: { show: true },
      axisLabel: { color: '#606266' }
    },
    yAxis: {
      type: 'category',
      data: difficulties,
      splitArea: { show: true },
      axisLabel: { color: '#606266' }
    },
    visualMap: {
      min: 0,
      max: 100,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: {
        color: ['#EBEEF5', '#B3D8FF', '#409EFF', '#337ECC', '#1A5694']
      },
      text: ['高', '低'],
      textStyle: { color: '#606266' }
    },
    series: [{
      type: 'heatmap',
      data: data,
      label: {
        show: true,
        formatter: (params) => params.value[2] + '%',
        color: '#fff',
        fontSize: 11
      },
      itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 }
    }]
  })
}

const initErrorPie = () => {
  if (!errorPieRef.value) return
  errorPieChart = echarts.init(errorPieRef.value)

  const errorData = [
    { value: 35, name: '语法错误', itemStyle: { color: '#F56C6C' } },
    { value: 28, name: '样式/布局问题', itemStyle: { color: '#E6A23C' } },
    { value: 18, name: '逻辑错误', itemStyle: { color: '#409EFF' } },
    { value: 12, name: '性能问题', itemStyle: { color: '#909399' } },
    { value: 7, name: '兼容性问题', itemStyle: { color: '#C0C4CC' } }
  ]

  errorPieChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#606266', fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' }
      },
      data: errorData
    }]
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

const getRateColor = (rate) => {
  if (rate >= 60) return '#F56C6C'
  if (rate >= 40) return '#E6A23C'
  return '#67C23A'
}

const handleMenuSelect = (index) => {
  activeMenu.value = index
}

const viewDetail = (row) => {
  ElMessage.info(`查看关卡详情: ${row.title}`)
}

const viewStudent = (row) => {
  router.push(`/teacher/student/${row.id}`)
}

// ========== 生命周期 ==========
onMounted(() => {
  nextTick(() => {
    initHeatmap()
    initErrorPie()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  heatmapChart?.dispose()
  errorPieChart?.dispose()
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  heatmapChart?.resize()
  errorPieChart?.resize()
}
</script>

<style scoped lang="scss">
.teacher-dashboard {
  display: flex;
  height: 100vh;
  background: #F0F2F5;
}

// 左侧导航
.dashboard-sidebar {
  width: 200px;
  background: #001529;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;

  :deep(.el-menu-item) {
    color: rgba(255, 255, 255, 0.65);

    &:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }

    &.is-active {
      color: #fff;
      background: #409EFF;
    }
  }
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

// 主内容区
.dashboard-main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

// 统计卡片
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  position: relative;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.stat-trend {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
  font-weight: 600;

  &.up { color: #67C23A; }
  &.down { color: #F56C6C; }
}

// 图表卡片
.charts-row {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
  margin-bottom: 20px;
}

.chart-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  padding: 20px;
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }
}

.chart-container {
  height: 320px;
}

// 表格样式
.challenge-name {
  display: flex;
  align-items: center;
}

.stuck-count {
  font-weight: 600;
  color: #303133;

  &.high {
    color: #F56C6C;
  }
}

.rate-cell {
  .el-progress {
    :deep(.el-progress__text) {
      font-size: 12px !important;
    }
  }
}

.student-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.student-avatar {
  background: #409EFF;
  color: #fff;
  font-size: 12px;
}

.stars-text {
  color: #E6A23C;
  font-weight: 500;
}

// 响应式
@media (max-width: 1366px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .dashboard-sidebar {
    width: 180px;
  }
}

@media (max-width: 1024px) {
  .dashboard-sidebar {
    width: 60px;

    .logo-text, .sidebar-footer, :deep(.el-menu-item span) {
      display: none;
    }
  }
}
</style>

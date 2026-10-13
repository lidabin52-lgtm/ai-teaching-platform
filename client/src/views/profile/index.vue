<template>
  <!-- 个人中心：展示用户信息和学习数据 -->
  <div class="profile-page">
    <h2 class="page-title">个人中心</h2>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="user-card">
          <div class="avatar">👤</div>
          <h3>开发者</h3>
          <p>前端学习之旅</p>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <template #header><span>学习统计</span></template>
          <!-- ECharts 图表挂载点 -->
          <div ref="chartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const chartRef = ref(null)

onMounted(() => {
  // ECharts 图表将在此处初始化
  console.log('图表容器已就绪，等待加载 ECharts...')
})
</script>

<style scoped lang="scss">
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  margin-bottom: 24px;
  color: $text-primary;
}

.user-card {
  text-align: center;

  .avatar {
    font-size: 64px;
    margin-bottom: 12px;
  }

  h3 {
    font-size: 18px;
    margin-bottom: 8px;
  }

  p {
    color: $text-secondary;
  }
}

.chart-container {
  height: 300px;
}
</style>

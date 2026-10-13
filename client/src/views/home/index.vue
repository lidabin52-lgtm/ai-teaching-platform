<template>
  <!-- 首页：展示平台概览、推荐课程和学习数据 -->
  <div class="home-page">
    <el-row :gutter="20">
      <!-- 欢迎区域 -->
      <el-col :span="24">
        <el-card class="welcome-card">
          <h2>欢迎来到 AI 前端智能教学与实战训练平台</h2>
          <p>基于大语言模型的智能学习体验，让前端学习更高效</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 功能入口 -->
    <el-row :gutter="20" class="feature-row">
      <el-col :span="6" v-for="feature in features" :key="feature.title">
        <el-card class="feature-card" shadow="hover" @click="$router.push(feature.path)">
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 功能模块入口配置
const features = ref([
  {
    title: '技能闯关',
    desc: '15个关卡，从青铜到王者，游戏化学习',
    icon: '🎮',
    path: '/challenge',
  },
  {
    title: '课程中心',
    desc: '系统化的前端课程体系，从基础到进阶',
    icon: '📚',
    path: '/course',
  },
  {
    title: '在线练习',
    desc: '自由编码练习，AI实时指导与反馈',
    icon: '💻',
    path: '/practice',
  },
  {
    title: 'AI助手',
    desc: '智能问答、代码分析、学习路径推荐',
    icon: '🤖',
    path: '/ai-assistant',
  },
])
</script>

<style scoped lang="scss">
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 20px;

  h2 {
    font-size: 28px;
    color: $primary-color;
    margin-bottom: 12px;
  }

  p {
    font-size: 16px;
    color: $text-secondary;
  }
}

.feature-row {
  margin-top: 20px;
}

.feature-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s;

  &:hover {
    transform: translateY(-4px);
  }

  .feature-icon {
    font-size: 48px;
    margin-bottom: 12px;
  }

  h3 {
    font-size: 18px;
    margin-bottom: 8px;
    color: $text-primary;
  }

  p {
    font-size: 14px;
    color: $text-secondary;
  }
}
</style>

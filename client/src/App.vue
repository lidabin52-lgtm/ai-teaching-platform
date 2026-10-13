<template>
  <!-- 应用根组件：包含顶部导航和主内容区域 -->
  <div class="app-layout">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="app-header">
        <div class="header-left">
          <h1 class="app-title" @click="$router.push(isTeacher ? '/teacher' : '/')" style="cursor:pointer">
            AI前端智能教学平台
          </h1>
        </div>
        <div class="header-center">
          <el-menu mode="horizontal" :default-active="activeMenu" router>
            <!-- 学生端菜单 -->
            <template v-if="!isTeacher">
              <el-menu-item index="/">首页</el-menu-item>
              <el-menu-item index="/challenge">技能闯关</el-menu-item>
              <el-menu-item index="/course">课程中心</el-menu-item>
              <el-menu-item index="/practice">在线练习</el-menu-item>
              <el-menu-item index="/ai-assistant">AI助手</el-menu-item>
            </template>
            <!-- 教师端菜单 -->
            <template v-else>
              <el-menu-item index="/teacher">学情概览</el-menu-item>
              <el-menu-item index="/challenge">关卡管理</el-menu-item>
              <el-menu-item index="/course">课程中心</el-menu-item>
            </template>
          </el-menu>
        </div>
        <div class="header-right">
          <!-- 已登录：显示用户信息和退出 -->
          <template v-if="isLoggedIn">
            <el-dropdown trigger="click" @command="handleCommand">
              <div class="user-info">
                <el-avatar :size="32" :src="userStore.userInfo?.avatar">
                  {{ userStore.userInfo?.nickname?.[0] || '?' }}
                </el-avatar>
                <span class="user-name">{{ userStore.userInfo?.nickname || '用户' }}</span>
                <el-tag :type="isTeacher ? 'warning' : 'primary'" size="small">
                  {{ isTeacher ? '教师' : '学生' }}
                </el-tag>
                <el-icon><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="!isTeacher" command="profile">
                    <el-icon><User /></el-icon> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item v-if="isTeacher" command="teacher">
                    <el-icon><DataAnalysis /></el-icon> 学情分析
                  </el-dropdown-item>
                  <el-dropdown-item v-if="!isTeacher && isTeacher" command="student">
                    <el-icon><Monitor /></el-icon> 学生端
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <!-- 未登录：显示登录按钮 -->
          <template v-else>
            <el-button type="primary" @click="$router.push('/login')">登录</el-button>
          </template>
        </div>
      </el-header>

      <!-- 主内容区域 -->
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ArrowDown, User, SwitchButton, DataAnalysis, Monitor } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 当前激活的菜单项
const activeMenu = computed(() => {
  const path = route.path
  // 教师端统一高亮
  if (path.startsWith('/teacher')) return '/teacher'
  return path
})

// 是否已登录
const isLoggedIn = computed(() => !!userStore.token)

// 是否是教师
const isTeacher = computed(() => userStore.userInfo?.role === 'teacher')

// 下拉菜单命令处理
const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'teacher':
      router.push('/teacher')
      break
    case 'student':
      router.push('/')
      break
    case 'logout':
      userStore.logout()
      localStorage.removeItem('userRole')
      ElMessage.success('已退出登录')
      router.push('/login')
      break
  }
}
</script>

<style scoped lang="scss">
.app-layout {
  width: 100%;
  height: 100%;
}

.app-header {
  display: flex;
  align-items: center;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;
  height: 60px;
  z-index: 100;

  .app-title {
    font-size: 18px;
    color: #409eff;
    white-space: nowrap;
    margin-right: 30px;
  }

  .header-center {
    flex: 1;

    :deep(.el-menu) {
      border-bottom: none;
    }
  }

  .header-right {
    display: flex;
    align-items: center;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background 0.2s;

  &:hover {
    background: #f5f7fa;
  }

  .user-name {
    font-size: 14px;
    color: #303133;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.app-main {
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
  padding: 20px;
}
</style>

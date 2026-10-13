<template>
  <!-- 登录页面 -->
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>🎓 AI前端智能教学平台</h1>
        <p>基于大语言模型的智能学习体验</p>
      </div>

      <el-card class="login-card">
        <el-tabs v-model="loginType" class="login-tabs">
          <!-- 账号登录 -->
          <el-tab-pane label="账号登录" name="account">
            <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="0">
              <el-form-item prop="username">
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                  @keyup.enter="handleLogin"
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  size="large"
                  style="width: 100%"
                  :loading="isLogging"
                  @click="handleLogin"
                >
                  登 录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- 快速体验 -->
          <el-tab-pane label="快速体验" name="quick">
            <div class="quick-login">
              <p class="quick-title">选择角色快速进入（无需密码）</p>
              <div class="role-cards">
                <div class="role-card student" @click="quickLogin('student1', 'student')">
                  <div class="role-icon">👨‍🎓</div>
                  <div class="role-info">
                    <h3>学生端</h3>
                    <p>体验闯关学习、AI导师等功能</p>
                  </div>
                  <el-icon><ArrowRight /></el-icon>
                </div>
                <div class="role-card teacher" @click="quickLogin('admin', 'teacher')">
                  <div class="role-icon">👨‍🏫</div>
                  <div class="role-info">
                    <h3>教师端</h3>
                    <p>查看学情分析、学生详情等功能</p>
                  </div>
                  <el-icon><ArrowRight /></el-icon>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <div class="login-footer">
        <p>默认账号：admin / 123456（教师）| student1~5 / 123456（学生）</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const loginType = ref('account')
const loginFormRef = ref(null)
const isLogging = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 账号登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return

    isLogging.value = true
    try {
      // 尝试调用后端API
      try {
        const res = await fetch('/api/user/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(loginForm)
        })
        if (res.ok) {
          const data = await res.json()
          if (data.code === 200) {
            const { token, user } = data.data
            userStore.setToken(token)
            userStore.setUserInfo(user)
            localStorage.setItem('userRole', user.role)
            redirectByRole(user.role)
            return
          }
        }
      } catch (e) {
        // 后端不可用，使用本地验证
      }

      // 本地Mock验证
      const validAccounts = [
        { username: 'admin', password: '123456', role: 'teacher', nickname: '管理员老师' },
        { username: 'student1', password: '123456', role: 'student', nickname: '学生1号' },
        { username: 'student2', password: '123456', role: 'student', nickname: '学生2号' },
        { username: 'student3', password: '123456', role: 'student', nickname: '学生3号' },
        { username: 'student4', password: '123456', role: 'student', nickname: '学生4号' },
        { username: 'student5', password: '123456', role: 'student', nickname: '学生5号' },
      ]

      const account = validAccounts.find(
        a => a.username === loginForm.username && a.password === loginForm.password
      )

      if (account) {
        userStore.setToken('mock-token-' + account.username)
        userStore.setUserInfo({
          id: account.username,
          username: account.username,
          role: account.role,
          nickname: account.nickname,
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${account.username}`
        })
        localStorage.setItem('userRole', account.role)
        ElMessage.success(`欢迎回来，${account.nickname}！`)
        redirectByRole(account.role)
      } else {
        ElMessage.error('用户名或密码错误')
      }
    } finally {
      isLogging.value = false
    }
  })
}

// 快速登录
const quickLogin = (username, role) => {
  const nicknames = {
    admin: '管理员老师',
    student1: '学生1号',
  }

  userStore.setToken('mock-token-' + username)
  userStore.setUserInfo({
    id: username,
    username: username,
    role: role,
    nickname: nicknames[username] || username,
    avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}`
  })
  localStorage.setItem('userRole', role)
  ElMessage.success(`已以${role === 'teacher' ? '教师' : '学生'}身份登录`)
  redirectByRole(role)
}

// 根据角色跳转
const redirectByRole = (role) => {
  if (role === 'teacher') {
    router.push('/teacher')
  } else {
    router.push('/')
  }
}
</script>

<style scoped lang="scss">
.login-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  width: 440px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;

  h1 {
    color: #fff;
    font-size: 32px;
    margin-bottom: 10px;
  }

  p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 16px;
  }
}

.login-card {
  border-radius: 12px;

  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
}

.quick-login {
  .quick-title {
    text-align: center;
    color: #909399;
    margin-bottom: 20px;
    font-size: 14px;
  }
}

.role-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-card {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;

  &.student {
    background: #ecf5ff;
    &:hover { border-color: #409eff; transform: translateY(-2px); }
  }

  &.teacher {
    background: #fdf6ec;
    &:hover { border-color: #e6a23c; transform: translateY(-2px); }
  }

  .role-icon {
    font-size: 36px;
    margin-right: 16px;
  }

  .role-info {
    flex: 1;

    h3 {
      font-size: 16px;
      margin-bottom: 4px;
      color: #303133;
    }

    p {
      font-size: 12px;
      color: #909399;
    }
  }

  .el-icon {
    font-size: 18px;
    color: #c0c4cc;
  }
}

.login-footer {
  text-align: center;
  margin-top: 20px;

  p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
  }
}
</style>

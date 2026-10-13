/**
 * Vue Router 路由配置
 * 定义应用的页面路由和导航守卫
 */
import { createRouter, createWebHistory } from 'vue-router'

// 路由规则定义
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', guest: true },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/index.vue'),
    meta: { title: '首页' },
  },
  {
    path: '/course',
    name: 'Course',
    component: () => import('@/views/course/index.vue'),
    meta: { title: '课程中心' },
  },
  {
    path: '/course/:id',
    name: 'CourseDetail',
    component: () => import('@/views/course/detail.vue'),
    meta: { title: '课程详情' },
  },
  {
    path: '/challenge',
    name: 'ChallengeList',
    component: () => import('@/views/challenge/ChallengeList.vue'),
    meta: { title: '技能闯关' },
  },
  {
    path: '/challenge/:id',
    name: 'ChallengePage',
    component: () => import('@/views/challenge/ChallengePage.vue'),
    meta: { title: '闯关练习' },
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/views/practice/index.vue'),
    meta: { title: '在线练习' },
  },
  {
    path: '/ai-assistant',
    name: 'AIAssistant',
    component: () => import('@/views/ai-assistant/index.vue'),
    meta: { title: 'AI助手' },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/index.vue'),
    meta: { title: '个人中心' },
  },
  // ========== 教师端路由 ==========
  {
    path: '/teacher',
    name: 'TeacherDashboard',
    component: () => import('@/views/teacher/TeacherDashboard.vue'),
    meta: { title: '学情分析', requiresRole: 'teacher' },
  },
  {
    path: '/teacher/student/:id',
    name: 'StudentDetail',
    component: () => import('@/views/teacher/StudentDetail.vue'),
    meta: { title: '学生详情', requiresRole: 'teacher' },
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'AI前端智能教学平台'} - AI前端智能教学与实战训练平台`

  const userRole = localStorage.getItem('userRole')
  const isLoggedIn = !!localStorage.getItem('token')

  // 已登录用户访问登录页，跳转首页
  if (to.meta.guest && isLoggedIn) {
    return next(userRole === 'teacher' ? '/teacher' : '/')
  }

  // 需要教师权限的页面
  if (to.meta.requiresRole === 'teacher') {
    if (userRole !== 'teacher') {
      // 非教师，跳转登录页
      return next('/login')
    }
  }

  next()
})

export default router

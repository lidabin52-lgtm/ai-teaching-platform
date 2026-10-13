/**
 * 应用入口文件
 * 初始化Vue实例、注册全局插件、挂载路由和状态管理
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'
import '@/assets/styles/global.scss'

// 创建Vue应用实例
const app = createApp(App)

// 注册插件
app.use(createPinia())   // 状态管理
app.use(router)           // 路由
app.use(ElementPlus, {    // Element Plus 组件库（中文语言包）
  locale: zhCn,
})

// 挂载应用
app.mount('#app')

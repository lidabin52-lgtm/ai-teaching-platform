/**
 * Pinia 状态管理 - 用户模块
 * 管理用户登录状态、个人信息等
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const userInfo = ref(null)
  // 登录令牌
  const token = ref(localStorage.getItem('token') || '')

  /**
   * 设置用户信息
   * @param {Object} info - 用户信息对象
   */
  function setUserInfo(info) {
    userInfo.value = info
  }

  /**
   * 设置登录令牌
   * @param {string} newToken - JWT令牌
   */
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  /**
   * 退出登录，清除状态
   */
  function logout() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return { userInfo, token, setUserInfo, setToken, logout }
})

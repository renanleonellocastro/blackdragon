import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('bd_token'))
  const user = ref<UserInfo | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  function setAuth(accessToken: string, userInfo: UserInfo) {
    token.value = accessToken
    user.value = userInfo
    localStorage.setItem('bd_token', accessToken)
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('bd_token')
  }

  function setUser(userInfo: UserInfo) {
    user.value = userInfo
  }

  return { token, user, isAuthenticated, isAdmin, setAuth, clearAuth, setUser }
})

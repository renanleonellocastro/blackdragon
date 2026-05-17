import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import * as authService from '@/services/auth.service'
import type { LoginPayload, RegisterPayload } from '@/services/auth.service'

export function useAuth() {
  const store = useAuthStore()
  const router = useRouter()

  async function login(payload: LoginPayload) {
    const response = await authService.login(payload)
    store.setAuth(response.access_token, response.user)
    router.push('/portal')
  }

  async function register(payload: RegisterPayload) {
    const response = await authService.register(payload)
    store.setAuth(response.access_token, response.user)
    router.push('/portal')
  }

  async function logout() {
    store.clearAuth()
    router.push('/login')
  }

  async function fetchUser() {
    try {
      const user = await authService.getMe()
      store.setUser(user)
    } catch {
      store.clearAuth()
    }
  }

  return {
    login,
    register,
    logout,
    fetchUser,
    isAuthenticated: store.isAuthenticated,
    isAdmin: store.isAdmin,
    user: store.user,
  }
}

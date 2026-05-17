import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const store_: Record<string, string> = {}
const mockStorage = {
  getItem: vi.fn((k: string) => store_[k] ?? null),
  setItem: vi.fn((k: string, v: string) => { store_[k] = v }),
  removeItem: vi.fn((k: string) => { delete store_[k] }),
}
Object.defineProperty(globalThis, 'localStorage', { value: mockStorage, writable: true })

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    Object.keys(store_).forEach((k) => delete store_[k])
    vi.clearAllMocks()
  })

  it('starts unauthenticated', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
  })

  it('setAuth sets token and user', () => {
    const store = useAuthStore()
    store.setAuth('test-token', {
      id: '1', email: 'a@b.com', full_name: 'Test', role: 'client',
    } as any)
    expect(store.isAuthenticated).toBe(true)
    expect(store.token).toBe('test-token')
    expect(store.user?.email).toBe('a@b.com')
  })

  it('clearAuth resets state', () => {
    const store = useAuthStore()
    store.setAuth('tok', { id: '1', email: 'a@b.com', full_name: 'X', role: 'client' } as any)
    store.clearAuth()
    expect(store.isAuthenticated).toBe(false)
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
  })

  it('isAdmin is true for admin role', () => {
    const store = useAuthStore()
    store.setAuth('tok', { id: '1', email: 'a@b.com', full_name: 'Admin', role: 'admin' } as any)
    expect(store.isAdmin).toBe(true)
  })

  it('isAdmin is false for client role', () => {
    const store = useAuthStore()
    store.setAuth('tok', { id: '1', email: 'a@b.com', full_name: 'Client', role: 'client' } as any)
    expect(store.isAdmin).toBe(false)
  })

  it('persists token to localStorage', () => {
    const store = useAuthStore()
    store.setAuth('persist-token', { id: '1', email: 'a@b.com', full_name: 'X', role: 'client' } as any)
    expect(localStorage.getItem('bd_token')).toBe('persist-token')
  })

  it('clears token from localStorage on clearAuth', () => {
    const store = useAuthStore()
    store.setAuth('tok', { id: '1', email: 'a@b.com', full_name: 'X', role: 'client' } as any)
    store.clearAuth()
    expect(localStorage.getItem('bd_token')).toBeFalsy()
  })
})

import { describe, it, expect } from 'vitest'
import api from '@/services/api'

describe('api service', () => {
  it('has /api baseURL', () => {
    expect(api.defaults.baseURL).toBe('/api')
  })

  it('has Content-Type json header', () => {
    expect(api.defaults.headers['Content-Type']).toBe('application/json')
  })

  it('has request and response interceptors', () => {
    // Axios stores interceptors as handlers array
    expect(api.interceptors.request).toBeDefined()
    expect(api.interceptors.response).toBeDefined()
  })
})

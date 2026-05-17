import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: attach auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle 401 session expiry
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const currentPath = window.location.pathname
      // Only redirect if we're in the portal (not public pages)
      if (currentPath.startsWith('/portal')) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`
      }
    }
    return Promise.reject(error)
  },
)

export default api

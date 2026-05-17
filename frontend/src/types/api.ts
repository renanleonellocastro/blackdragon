export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface ApiError {
  detail: string
  status_code: number
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: string
  email: string
  full_name: string
  role: 'client' | 'admin'
  tenant_id: string
  is_active: boolean
}

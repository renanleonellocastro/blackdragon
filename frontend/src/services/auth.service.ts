import api from '@/services/api'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  full_name: string
  company_name?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

export interface UserInfo {
  id: string
  email: string
  full_name: string
  role: string
  tenant_id: string
  last_login_at: string | null
  created_at: string
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/auth/login', payload)
  return data
}

export async function register(payload: RegisterPayload): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>('/auth/register', payload)
  return data
}

export async function refreshToken(): Promise<{ access_token: string; token_type: string }> {
  const { data } = await api.post('/auth/refresh')
  return data
}

export async function getMe(): Promise<UserInfo> {
  const { data } = await api.get<UserInfo>('/auth/me')
  return data
}

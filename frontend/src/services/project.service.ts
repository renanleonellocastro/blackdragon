import api from '@/services/api'

export interface ProjectItem {
  id: string
  name: string
  description: string | null
  status: string
  property_id: string
  current_version: number
  is_locked: boolean
  locked_by: string | null
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
  property_id: string
}

export interface ProjectUpdate {
  name?: string
  description?: string
  status?: string
}

export async function listProjects(propertyId?: string, status?: string): Promise<ProjectItem[]> {
  const params: Record<string, string> = {}
  if (propertyId) params.property_id = propertyId
  if (status) params.status = status
  const { data } = await api.get<ProjectItem[]>('/projects', { params })
  return data
}

export async function getProject(id: string): Promise<ProjectItem> {
  const { data } = await api.get<ProjectItem>(`/projects/${id}`)
  return data
}

export async function createProject(payload: ProjectCreate): Promise<ProjectItem> {
  const { data } = await api.post<ProjectItem>('/projects', payload)
  return data
}

export async function updateProject(id: string, payload: ProjectUpdate): Promise<ProjectItem> {
  const { data } = await api.patch<ProjectItem>(`/projects/${id}`, payload)
  return data
}

export async function deleteProject(id: string): Promise<void> {
  await api.delete(`/projects/${id}`)
}

export async function duplicateProject(id: string): Promise<ProjectItem> {
  const { data } = await api.post<ProjectItem>(`/projects/${id}/duplicate`)
  return data
}

import api from '@/services/api'

export interface DeployResponse {
  id: string
  status: string
  board_instance_id: string
  artifact_id: string
  progress_percent: number
  started_at: string
}

export interface DeploymentItem {
  id: string
  status: string
  progress_percent: number
  error_message: string | null
  started_at: string
  completed_at: string | null
}

export async function deploy(projectId: string, artifactId: string, boardInstanceId: string): Promise<DeployResponse> {
  const { data } = await api.post<DeployResponse>(`/projects/${projectId}/deployments`, {
    artifact_id: artifactId,
    board_instance_id: boardInstanceId,
  })
  return data
}

export async function listDeployments(projectId: string): Promise<DeploymentItem[]> {
  const { data } = await api.get<DeploymentItem[]>(`/projects/${projectId}/deployments`)
  return data
}

export async function getDeployment(projectId: string, deploymentId: string): Promise<DeploymentItem> {
  const { data } = await api.get<DeploymentItem>(`/projects/${projectId}/deployments/${deploymentId}`)
  return data
}

export async function cancelDeployment(projectId: string, deploymentId: string): Promise<DeploymentItem> {
  const { data } = await api.post<DeploymentItem>(`/projects/${projectId}/deployments/${deploymentId}/cancel`)
  return data
}

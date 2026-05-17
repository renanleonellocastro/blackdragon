import api from '@/services/api'

export interface CompileResponse {
  success: boolean
  validation: ValidationResult
  output: string | null
  artifact_id: string | null
}

export interface ValidationResult {
  valid: boolean
  errors: ValidationError[]
  warnings: ValidationError[]
}

export interface ValidationError {
  node_id: string | null
  message: string
  severity: string
}

export interface ArtifactResponse {
  id: string
  diagram_id: string
  target: string
  version: number
  output: string
  node_count: number
  edge_count: number
  created_at: string
}

export async function compile(diagramId: string, context?: Record<string, unknown>): Promise<CompileResponse> {
  const { data } = await api.post<CompileResponse>('/compiler/compile', {
    diagram_id: diagramId,
    context: context || {},
  })
  return data
}

export async function validate(diagramId: string): Promise<ValidationResult> {
  const { data } = await api.post<ValidationResult>('/compiler/validate', {
    diagram_id: diagramId,
  })
  return data
}

export async function getArtifact(artifactId: string): Promise<ArtifactResponse> {
  const { data } = await api.get<ArtifactResponse>(`/compiler/artifacts/${artifactId}`)
  return data
}

export function getDownloadUrl(artifactId: string): string {
  return `/api/compiler/artifacts/${artifactId}/download`
}

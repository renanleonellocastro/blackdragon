export interface ProjectType {
  id: string
  name: string
  description: string | null
  status: 'draft' | 'active' | 'archived'
  property_id: string
  current_version: number
  is_locked: boolean
  locked_by: string | null
  created_at: string
  updated_at: string
}

export interface PropertyType {
  id: string
  name: string
  address: string | null
  description: string | null
  created_at: string
  updated_at: string
}

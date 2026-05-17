import api from '@/services/api'

export interface BoardModel {
  id: string
  name: string
  slug: string
  description: string | null
  platform: string
  board_variant: string
  image_url: string | null
  is_active: boolean
  channels: BoardModelChannel[]
}

export interface BoardModelChannel {
  id: string
  channel_number: number
  direction: string
  default_gpio_pin: number
  supports_pullup: boolean
  supports_pulldown: boolean
  supports_pwm: boolean
  label: string | null
}

export interface BoardInstance {
  id: string
  name: string
  esphome_name: string
  device_address: string | null
  board_model_id: string
  channels: BoardInstanceChannel[]
}

export interface BoardInstanceChannel {
  id: string
  channel_number: number
  direction: string
  name: string
  gpio_pin: number
  pull_mode: string
  inverted: boolean
  debounce_ms: number
  is_enabled: boolean
}

export async function listCatalog(): Promise<BoardModel[]> {
  const { data } = await api.get<BoardModel[]>('/boards/catalog')
  return data
}

export async function listInstances(projectId: string): Promise<BoardInstance[]> {
  const { data } = await api.get<BoardInstance[]>(`/boards/projects/${projectId}/instances`)
  return data
}

export async function createInstance(
  projectId: string,
  payload: { board_model_id: string; name: string; esphome_name: string; device_address?: string },
): Promise<BoardInstance> {
  const { data } = await api.post<BoardInstance>(`/boards/projects/${projectId}/instances`, payload)
  return data
}

export async function updateChannel(
  instanceId: string,
  config: { channel_number: number; name?: string; gpio_pin?: number; pull_mode?: string; inverted?: boolean; debounce_ms?: number; is_enabled?: boolean },
): Promise<void> {
  await api.patch(`/boards/instances/${instanceId}/channels`, config)
}

export async function deleteInstance(instanceId: string): Promise<void> {
  await api.delete(`/boards/instances/${instanceId}`)
}

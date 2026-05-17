export interface BoardType {
  id: string
  name: string
  slug: string
  description: string | null
  platform: string
  board_variant: string
  channels: BoardChannelType[]
}

export interface BoardChannelType {
  id: string
  channel_number: number
  direction: 'input' | 'output'
  gpio_pin: number
  name: string
  pull_mode: string
  inverted: boolean
  debounce_ms: number
  is_enabled: boolean
}

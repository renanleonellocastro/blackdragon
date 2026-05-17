export interface PortDefinition {
  id: string
  label: string
  type: 'signal' | 'boolean' | 'number'
  direction: 'input' | 'output'
  color: string
}

export interface NodeDefinition {
  type: string
  label: string
  category: 'Hardware' | 'Logic' | 'Timing' | 'Constants'
  inputs: PortDefinition[]
  outputs: PortDefinition[]
  properties: NodeProperty[]
}

export interface NodeProperty {
  key: string
  label: string
  type: 'string' | 'number' | 'boolean' | 'select'
  default?: string | number | boolean
  options?: string[]
}

export interface NodeData {
  type: string
  label: string
  properties: Record<string, string | number | boolean>
  [key: string]: unknown
}

export interface EdgeData {
  id: string
  source: string
  sourceHandle: string
  target: string
  targetHandle: string
}

export const NODE_DEFINITIONS: NodeDefinition[] = [
  {
    type: 'digital-input',
    label: 'Digital Input',
    category: 'Hardware',
    inputs: [],
    outputs: [{ id: 'signal', label: 'Signal', type: 'signal', direction: 'output', color: '#10B981' }],
    properties: [
      { key: 'gpio_pin', label: 'GPIO Pin', type: 'number', default: 0 },
      { key: 'pull_mode', label: 'Pull Mode', type: 'select', default: 'none', options: ['none', 'up', 'down'] },
      { key: 'inverted', label: 'Inverted', type: 'boolean', default: false },
    ],
  },
  {
    type: 'digital-output',
    label: 'Digital Output',
    category: 'Hardware',
    inputs: [{ id: 'signal', label: 'Signal', type: 'signal', direction: 'input', color: '#F59E0B' }],
    outputs: [],
    properties: [
      { key: 'gpio_pin', label: 'GPIO Pin', type: 'number', default: 0 },
      { key: 'inverted', label: 'Inverted', type: 'boolean', default: false },
    ],
  },
  {
    type: 'and-gate',
    label: 'AND Gate',
    category: 'Logic',
    inputs: [
      { id: 'a', label: 'A', type: 'boolean', direction: 'input', color: '#D1D5DB' },
      { id: 'b', label: 'B', type: 'boolean', direction: 'input', color: '#D1D5DB' },
    ],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#D1D5DB' }],
    properties: [],
  },
  {
    type: 'or-gate',
    label: 'OR Gate',
    category: 'Logic',
    inputs: [
      { id: 'a', label: 'A', type: 'boolean', direction: 'input', color: '#D1D5DB' },
      { id: 'b', label: 'B', type: 'boolean', direction: 'input', color: '#D1D5DB' },
    ],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#D1D5DB' }],
    properties: [],
  },
  {
    type: 'not-gate',
    label: 'NOT Gate',
    category: 'Logic',
    inputs: [{ id: 'in', label: 'In', type: 'boolean', direction: 'input', color: '#D1D5DB' }],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#D1D5DB' }],
    properties: [],
  },
  {
    type: 'xor-gate',
    label: 'XOR Gate',
    category: 'Logic',
    inputs: [
      { id: 'a', label: 'A', type: 'boolean', direction: 'input', color: '#D1D5DB' },
      { id: 'b', label: 'B', type: 'boolean', direction: 'input', color: '#D1D5DB' },
    ],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#D1D5DB' }],
    properties: [],
  },
  {
    type: 'timer',
    label: 'Timer',
    category: 'Timing',
    inputs: [{ id: 'trigger', label: 'Trigger', type: 'signal', direction: 'input', color: '#6B7280' }],
    outputs: [{ id: 'out', label: 'Out', type: 'signal', direction: 'output', color: '#10B981' }],
    properties: [{ key: 'duration_ms', label: 'Duration (ms)', type: 'number', default: 1000 }],
  },
  {
    type: 'delay',
    label: 'Delay',
    category: 'Timing',
    inputs: [{ id: 'in', label: 'In', type: 'signal', direction: 'input', color: '#6B7280' }],
    outputs: [{ id: 'out', label: 'Out', type: 'signal', direction: 'output', color: '#6B7280' }],
    properties: [{ key: 'delay_ms', label: 'Delay (ms)', type: 'number', default: 500 }],
  },
  {
    type: 'edge-detector',
    label: 'Edge Detector',
    category: 'Timing',
    inputs: [{ id: 'in', label: 'In', type: 'signal', direction: 'input', color: '#6B7280' }],
    outputs: [
      { id: 'rising', label: 'Rising', type: 'signal', direction: 'output', color: '#10B981' },
      { id: 'falling', label: 'Falling', type: 'signal', direction: 'output', color: '#EF4444' },
    ],
    properties: [],
  },
  {
    type: 'debounce',
    label: 'Debounce',
    category: 'Timing',
    inputs: [{ id: 'in', label: 'In', type: 'signal', direction: 'input', color: '#6B7280' }],
    outputs: [{ id: 'out', label: 'Out', type: 'signal', direction: 'output', color: '#6B7280' }],
    properties: [{ key: 'delay_ms', label: 'Delay (ms)', type: 'number', default: 50 }],
  },
  {
    type: 'constant-true',
    label: 'Constant TRUE',
    category: 'Constants',
    inputs: [],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#10B981' }],
    properties: [],
  },
  {
    type: 'constant-false',
    label: 'Constant FALSE',
    category: 'Constants',
    inputs: [],
    outputs: [{ id: 'out', label: 'Out', type: 'boolean', direction: 'output', color: '#EF4444' }],
    properties: [],
  },
]

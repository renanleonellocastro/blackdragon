import { describe, it, expect } from 'vitest'
import { NODE_DEFINITIONS } from '@/types/editor'

describe('NODE_DEFINITIONS', () => {
  it('has at least 10 node definitions', () => {
    expect(NODE_DEFINITIONS.length).toBeGreaterThanOrEqual(10)
  })

  it('includes all hardware nodes', () => {
    const types = NODE_DEFINITIONS.map((d) => d.type)
    expect(types).toContain('digital-input')
    expect(types).toContain('digital-output')
  })

  it('includes logic gates', () => {
    const types = NODE_DEFINITIONS.map((d) => d.type)
    expect(types).toContain('and-gate')
    expect(types).toContain('or-gate')
    expect(types).toContain('not-gate')
    expect(types).toContain('xor-gate')
  })

  it('includes timing nodes', () => {
    const types = NODE_DEFINITIONS.map((d) => d.type)
    expect(types).toContain('timer')
    expect(types).toContain('delay')
    expect(types).toContain('debounce')
    expect(types).toContain('edge-detector')
  })

  it('includes constant nodes', () => {
    const types = NODE_DEFINITIONS.map((d) => d.type)
    expect(types).toContain('constant-true')
    expect(types).toContain('constant-false')
  })

  it('all definitions have valid categories', () => {
    const validCategories = ['Hardware', 'Logic', 'Timing', 'Constants']
    for (const def of NODE_DEFINITIONS) {
      expect(validCategories).toContain(def.category)
    }
  })

  it('all definitions have at least one port', () => {
    for (const def of NODE_DEFINITIONS) {
      expect(def.inputs.length + def.outputs.length).toBeGreaterThan(0)
    }
  })

  it('digital-input has gpio_pin property', () => {
    const di = NODE_DEFINITIONS.find((d) => d.type === 'digital-input')!
    const gpioPin = di.properties.find((p) => p.key === 'gpio_pin')
    expect(gpioPin).toBeDefined()
    expect(gpioPin!.type).toBe('number')
  })
})

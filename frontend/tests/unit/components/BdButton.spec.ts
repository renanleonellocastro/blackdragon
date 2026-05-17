import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdButton from '@/components/ui/BdButton.vue'

describe('BdButton', () => {
  it('renders slot content', () => {
    const wrapper = mount(BdButton, { slots: { default: 'Click me' } })
    expect(wrapper.text()).toContain('Click me')
  })

  it('emits click event', async () => {
    const wrapper = mount(BdButton)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('applies metallic style by default', () => {
    const wrapper = mount(BdButton)
    expect(wrapper.html()).toContain('bd-metallic')
  })

  it('renders as button element', () => {
    const wrapper = mount(BdButton)
    expect(wrapper.element.tagName).toBe('BUTTON')
  })
})

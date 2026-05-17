import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'

describe('BdStatusIndicator', () => {
  it('renders badge label', () => {
    const wrapper = mount(BdStatusIndicator, {
      props: { status: 'success', variant: 'badge', label: 'Active' },
    })
    expect(wrapper.text()).toContain('Active')
  })

  it('renders dot variant', () => {
    const wrapper = mount(BdStatusIndicator, {
      props: { status: 'error', variant: 'dot' },
    })
    expect(wrapper.html()).toBeTruthy()
  })
})

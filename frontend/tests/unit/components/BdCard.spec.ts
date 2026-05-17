import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdCard from '@/components/ui/BdCard.vue'

describe('BdCard', () => {
  it('renders slot content', () => {
    const wrapper = mount(BdCard, { slots: { default: '<p>Card content</p>' } })
    expect(wrapper.text()).toContain('Card content')
  })

  it('has bg-bd-bg class', () => {
    const wrapper = mount(BdCard)
    expect(wrapper.html()).toContain('bd-bg')
  })
})

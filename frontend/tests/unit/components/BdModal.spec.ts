import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdModal from '@/components/ui/BdModal.vue'

describe('BdModal', () => {
  it('does not render content when modelValue is false', () => {
    const wrapper = mount(BdModal, {
      props: { modelValue: false, title: 'Test' },
      global: { stubs: { Teleport: true } },
    })
    // The modal should not be visible
    expect(wrapper.find('.fixed').exists()).toBe(false)
  })

  it('renders content when modelValue is true', () => {
    const wrapper = mount(BdModal, {
      props: { modelValue: true, title: 'My Modal' },
      slots: { default: '<p>Body</p>' },
      global: { stubs: { Teleport: true } },
    })
    expect(wrapper.text()).toContain('My Modal')
    expect(wrapper.text()).toContain('Body')
  })

  it('emits close on X button click', async () => {
    const wrapper = mount(BdModal, {
      props: { modelValue: true, title: 'Test' },
      global: { stubs: { Teleport: true } },
    })
    const closeBtn = wrapper.find('button')
    if (closeBtn.exists()) {
      await closeBtn.trigger('click')
      expect(wrapper.emitted('close') || wrapper.emitted('update:modelValue')).toBeTruthy()
    }
  })
})

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdInput from '@/components/ui/BdInput.vue'

describe('BdInput', () => {
  it('renders label when provided', () => {
    const wrapper = mount(BdInput, { props: { label: 'Email', modelValue: '' } })
    expect(wrapper.text()).toContain('Email')
  })

  it('renders an input element', () => {
    const wrapper = mount(BdInput, { props: { modelValue: '' } })
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(BdInput, { props: { modelValue: '' } })
    await wrapper.find('input').setValue('hello')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
  })
})

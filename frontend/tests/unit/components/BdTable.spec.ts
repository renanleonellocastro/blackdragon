import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BdTable from '@/components/ui/BdTable.vue'

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'status', label: 'Status' },
]

const data = [
  { name: 'Alpha', status: 'active' },
  { name: 'Beta', status: 'inactive' },
  { name: 'Charlie', status: 'active' },
]

describe('BdTable', () => {
  it('renders column headers', () => {
    const wrapper = mount(BdTable, { props: { columns, data } })
    expect(wrapper.text()).toContain('Name')
    expect(wrapper.text()).toContain('Status')
  })

  it('renders data rows', () => {
    const wrapper = mount(BdTable, { props: { columns, data } })
    expect(wrapper.text()).toContain('Alpha')
    expect(wrapper.text()).toContain('Beta')
    expect(wrapper.text()).toContain('Charlie')
  })

  it('emits sort when clicking sortable column', async () => {
    const wrapper = mount(BdTable, { props: { columns, data } })
    const th = wrapper.findAll('th')[0]!
    await th.trigger('click')
    expect(wrapper.emitted('sort')?.[0]).toEqual(['name'])
  })

  it('does not emit sort for non-sortable columns', async () => {
    const wrapper = mount(BdTable, { props: { columns, data } })
    const th = wrapper.findAll('th')[1]!
    await th.trigger('click')
    expect(wrapper.emitted('sort')).toBeUndefined()
  })

  it('sorts data ascending by prop', () => {
    const wrapper = mount(BdTable, {
      props: { columns, data: data.slice().reverse(), sortBy: 'name', sortDir: 'asc' as const },
    })
    const rows = wrapper.findAll('tbody tr')
    expect(rows[0]!.text()).toContain('Alpha')
  })

  it('sorts data descending by prop', () => {
    const wrapper = mount(BdTable, {
      props: { columns, data, sortBy: 'name', sortDir: 'desc' as const },
    })
    const rows = wrapper.findAll('tbody tr')
    expect(rows[0]!.text()).toContain('Charlie')
  })

  it('renders empty table with no-data message', () => {
    const wrapper = mount(BdTable, { props: { columns, data: [] } })
    expect(wrapper.text()).toContain('No data available')
  })
})

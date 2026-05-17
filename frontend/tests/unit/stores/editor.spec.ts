import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useEditorStore } from '@/stores/editor'

describe('editor store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts with empty graph', () => {
    const store = useEditorStore()
    expect(store.nodes).toEqual([])
    expect(store.edges).toEqual([])
    expect(store.isDirty).toBe(false)
  })

  it('addNode adds a node and marks dirty', () => {
    const store = useEditorStore()
    store.addNode({
      id: 'n1',
      type: 'digital-input',
      position: { x: 0, y: 0 },
      data: { type: 'digital-input', label: 'Input', properties: { gpio_pin: 4 } },
    })
    expect(store.nodes).toHaveLength(1)
    expect(store.isDirty).toBe(true)
  })

  it('removeNode removes node and related edges', () => {
    const store = useEditorStore()
    store.addNode({ id: 'a', type: 'digital-input', position: { x: 0, y: 0 }, data: { type: 'digital-input', label: 'A', properties: {} } })
    store.addNode({ id: 'b', type: 'digital-output', position: { x: 100, y: 0 }, data: { type: 'digital-output', label: 'B', properties: {} } })
    store.addEdge({ id: 'e1', source: 'a', target: 'b' })
    store.removeNode('a')
    expect(store.nodes).toHaveLength(1)
    expect(store.edges).toHaveLength(0)
  })

  it('addEdge prevents duplicates', () => {
    const store = useEditorStore()
    store.addEdge({ id: 'e1', source: 'a', sourceHandle: 'out', target: 'b', targetHandle: 'in' })
    store.addEdge({ id: 'e1', source: 'a', sourceHandle: 'out', target: 'b', targetHandle: 'in' })
    expect(store.edges).toHaveLength(1)
  })

  it('selectNode updates selectedNodeId', () => {
    const store = useEditorStore()
    store.selectNode('n1')
    expect(store.selectedNodeId).toBe('n1')
    store.selectNode(null)
    expect(store.selectedNodeId).toBeNull()
  })

  it('updateNodeProperty updates existing node', () => {
    const store = useEditorStore()
    store.addNode({
      id: 'n1', type: 'digital-input', position: { x: 0, y: 0 },
      data: { type: 'digital-input', label: 'In', properties: { gpio_pin: 4 } },
    })
    store.updateNodeProperty('n1', 'gpio_pin', 5)
    expect(store.nodes[0]!.data.properties.gpio_pin).toBe(5)
  })

  it('clearGraph resets everything', () => {
    const store = useEditorStore()
    store.addNode({ id: 'n1', type: 'test', position: { x: 0, y: 0 }, data: { type: 'test', label: 'T', properties: {} } })
    store.clearGraph()
    expect(store.nodes).toHaveLength(0)
    expect(store.edges).toHaveLength(0)
    expect(store.isDirty).toBe(false)
  })

  it('getGraphData returns serialized form', () => {
    const store = useEditorStore()
    store.addNode({ id: 'n1', type: 'timer', position: { x: 10, y: 20 }, data: { type: 'timer', label: 'T', properties: {} } })
    store.addEdge({ id: 'e1', source: 'n1', sourceHandle: 'out', target: 'n2', targetHandle: 'in' })
    const graph = store.getGraphData()
    expect(graph.nodes).toHaveLength(1)
    expect(graph.edges).toHaveLength(1)
    expect(graph.nodes[0]!.position).toEqual({ x: 10, y: 20 })
  })

  it('loadGraph replaces current state', () => {
    const store = useEditorStore()
    store.addNode({ id: 'old', type: 'test', position: { x: 0, y: 0 }, data: { type: 'test', label: 'Old', properties: {} } })
    store.loadGraph(
      [{ id: 'new', type: 'timer', position: { x: 5, y: 5 }, data: { type: 'timer', label: 'New', properties: {} } }],
      [{ id: 'e1', source: 'new', target: 'x' }],
    )
    expect(store.nodes).toHaveLength(1)
    expect(store.nodes[0]!.id).toBe('new')
    expect(store.isDirty).toBe(false)
  })
})

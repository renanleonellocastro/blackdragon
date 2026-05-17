import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { NodeData } from '@/types/editor'

interface EditorEdge {
  id: string
  source: string
  sourceHandle?: string
  target: string
  targetHandle?: string
  [key: string]: unknown
}

interface EditorNode {
  id: string
  type?: string
  position: { x: number; y: number }
  data: NodeData
  [key: string]: unknown
}

export const useEditorStore = defineStore('editor', () => {
  const nodes = ref<EditorNode[]>([])
  const edges = ref<EditorEdge[]>([])
  const selectedNodeId = ref<string | null>(null)
  const diagramId = ref<string | null>(null)
  const isDirty = ref(false)

  function addNode(node: EditorNode) {
    nodes.value.push(node)
    isDirty.value = true
  }

  function removeNode(nodeId: string) {
    nodes.value = nodes.value.filter((n) => n.id !== nodeId)
    edges.value = edges.value.filter((e) => e.source !== nodeId && e.target !== nodeId)
    if (selectedNodeId.value === nodeId) selectedNodeId.value = null
    isDirty.value = true
  }

  function addEdge(edge: EditorEdge) {
    // Prevent duplicate connections
    const exists = edges.value.some(
      (e) => e.source === edge.source && e.sourceHandle === edge.sourceHandle &&
        e.target === edge.target && e.targetHandle === edge.targetHandle,
    )
    if (!exists) {
      edges.value.push(edge)
      isDirty.value = true
    }
  }

  function removeEdge(edgeId: string) {
    edges.value = edges.value.filter((e) => e.id !== edgeId)
    isDirty.value = true
  }

  function updateNodeProperty(nodeId: string, key: string, value: string | number | boolean) {
    const node = nodes.value.find((n) => n.id === nodeId)
    if (node?.data) {
      node.data.properties[key] = value
      isDirty.value = true
    }
  }

  function selectNode(nodeId: string | null) {
    selectedNodeId.value = nodeId
  }

  function loadGraph(graphNodes: EditorNode[], graphEdges: EditorEdge[]) {
    nodes.value = graphNodes
    edges.value = graphEdges
    isDirty.value = false
  }

  function clearGraph() {
    nodes.value = []
    edges.value = []
    selectedNodeId.value = null
    diagramId.value = null
    isDirty.value = false
  }

  function getGraphData() {
    return {
      nodes: nodes.value.map((n) => ({
        id: n.id,
        type: n.type,
        position: n.position,
        data: n.data,
      })),
      edges: edges.value.map((e) => ({
        id: e.id,
        source: e.source,
        sourceHandle: e.sourceHandle,
        target: e.target,
        targetHandle: e.targetHandle,
      })),
    }
  }

  return {
    nodes, edges, selectedNodeId, diagramId, isDirty,
    addNode, removeNode, addEdge, removeEdge,
    updateNodeProperty, selectNode, loadGraph, clearGraph, getGraphData,
  }
})

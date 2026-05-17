<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import BdButton from '@/components/ui/BdButton.vue'
import EditorCanvas from '@/components/editor/EditorCanvas.vue'
import NodePalette from '@/components/editor/NodePalette.vue'
import PropertiesPanel from '@/components/editor/PropertiesPanel.vue'
import { useEditorStore } from '@/stores/editor'
import { useAutoSave } from '@/composables/useAutoSave'
import type { NodeDefinition } from '@/types/editor'
import api from '@/services/api'

const route = useRoute()
const projectId = route.params.id as string
const store = useEditorStore()
const { lastSaved } = useAutoSave(projectId)

const diagramName = ref('Untitled Diagram')
let nodeCounter = 0

onMounted(async () => {
  // Load first diagram or create one
  try {
    const { data: diagrams } = await api.get(`/projects/${projectId}/diagrams`)
    if (diagrams.length > 0) {
      const { data } = await api.get(`/projects/${projectId}/diagrams/${diagrams[0].id}`)
      store.diagramId = data.id
      diagramName.value = data.name
      if (data.graph_data?.nodes) {
        store.loadGraph(data.graph_data.nodes, data.graph_data.edges || [])
      }
    }
  } catch {
    // New project with no diagrams
  }
})

function addNode(def: NodeDefinition) {
  nodeCounter++
  const id = `${def.type}-${nodeCounter}`
  const properties: Record<string, string | number | boolean> = {}
  for (const prop of def.properties) {
    properties[prop.key] = prop.default ?? ''
  }
  store.addNode({
    id,
    type: def.type,
    position: { x: 200 + Math.random() * 200, y: 100 + Math.random() * 200 },
    data: { type: def.type, label: def.label, properties },
  })
}

async function save() {
  if (!store.diagramId) return
  await api.put(`/projects/${projectId}/diagrams/${store.diagramId}`, {
    graph_data: store.getGraphData(),
  })
  store.isDirty = false
}
</script>

<template>
  <div class="flex h-[calc(100vh-64px)] flex-col bg-bd-bg-primary">
    <!-- Toolbar -->
    <div class="flex items-center justify-between border-b border-bd-border bg-bd-bg-panel px-4 py-2">
      <div class="flex items-center gap-3">
        <h2 class="font-bd-sans text-sm font-semibold text-bd-text-primary">{{ diagramName }}</h2>
        <span v-if="store.isDirty" class="text-[10px] text-bd-warning">Unsaved</span>
        <span v-if="lastSaved" class="text-[10px] text-bd-text-muted">
          Auto-saved {{ lastSaved.toLocaleTimeString() }}
        </span>
      </div>
      <div class="flex gap-2">
        <BdButton size="sm" variant="secondary" @click="save" :disabled="!store.isDirty">
          Save
        </BdButton>
        <BdButton size="sm" variant="primary">Compile</BdButton>
      </div>
    </div>

    <!-- Main Editor Layout -->
    <div class="flex flex-1 overflow-hidden">
      <div class="w-56 shrink-0 border-r border-bd-border">
        <NodePalette @add-node="addNode" />
      </div>
      <div class="flex-1">
        <EditorCanvas />
      </div>
      <div class="w-64 shrink-0 border-l border-bd-border">
        <PropertiesPanel />
      </div>
    </div>
  </div>
</template>

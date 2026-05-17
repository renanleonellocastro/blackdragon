<script setup lang="ts">
import { VueFlow, type Connection } from '@vue-flow/core'
import { MiniMap } from '@vue-flow/minimap'
import { Controls } from '@vue-flow/controls'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/minimap/dist/style.css'
import '@vue-flow/controls/dist/style.css'

import DigitalInputNode from './nodes/DigitalInputNode.vue'
import DigitalOutputNode from './nodes/DigitalOutputNode.vue'
import LogicGateNode from './nodes/LogicGateNode.vue'
import TimerNode from './nodes/TimerNode.vue'
import DelayNode from './nodes/DelayNode.vue'
import EdgeDetectorNode from './nodes/EdgeDetectorNode.vue'
import DebounceNode from './nodes/DebounceNode.vue'
import ConstantNode from './nodes/ConstantNode.vue'
import { useEditorStore } from '@/stores/editor'

const store = useEditorStore()

const nodeTypes: Record<string, any> = {
  'digital-input': DigitalInputNode,
  'digital-output': DigitalOutputNode,
  'and-gate': LogicGateNode,
  'or-gate': LogicGateNode,
  'not-gate': LogicGateNode,
  'xor-gate': LogicGateNode,
  'timer': TimerNode,
  'delay': DelayNode,
  'edge-detector': EdgeDetectorNode,
  'debounce': DebounceNode,
  'constant-true': ConstantNode,
  'constant-false': ConstantNode,
}

function onConnect(connection: Connection) {
  store.addEdge({
    id: `e-${connection.source}-${connection.sourceHandle}-${connection.target}-${connection.targetHandle}`,
    source: connection.source,
    sourceHandle: connection.sourceHandle ?? undefined,
    target: connection.target,
    targetHandle: connection.targetHandle ?? undefined,
  })
}

function onNodeClick(event: { node: { id: string } }) {
  store.selectNode(event.node.id)
}

function onPaneClick() {
  store.selectNode(null)
}
</script>

<template>
  <div class="h-full w-full bg-bd-bg-primary" style="background-image: url('/circuit-pattern.svg'); background-size: 100px 100px; background-repeat: repeat;">
    <VueFlow
      v-model:nodes="store.nodes"
      v-model:edges="store.edges"
      :node-types="nodeTypes"
      :default-edge-options="{ style: { stroke: '#6B7280', strokeWidth: 2 }, animated: true }"
      :snap-to-grid="true"
      :snap-grid="[16, 16]"
      class="h-full w-full"
      @connect="onConnect"
      @node-click="onNodeClick"
      @pane-click="onPaneClick"
    >
      <MiniMap class="!bg-bd-bg-panel !border-bd-border" />
      <Controls class="!bg-bd-bg-panel !border-bd-border !text-bd-text-primary" />
    </VueFlow>
  </div>
</template>

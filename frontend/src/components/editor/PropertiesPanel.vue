<script setup lang="ts">
import { computed } from 'vue'
import BdInput from '@/components/ui/BdInput.vue'
import { useEditorStore } from '@/stores/editor'
import { NODE_DEFINITIONS } from '@/types/editor'

const store = useEditorStore()

const selectedNode = computed(() => {
  if (!store.selectedNodeId) return null
  return store.nodes.find((n) => n.id === store.selectedNodeId) ?? null
})

const nodeDef = computed(() => {
  if (!selectedNode.value) return null
  return NODE_DEFINITIONS.find((d) => d.type === selectedNode.value!.type) ?? null
})

function updateProperty(key: string, value: string | number | boolean) {
  if (selectedNode.value) {
    store.updateNodeProperty(selectedNode.value.id, key, value)
  }
}
</script>

<template>
  <div class="flex h-full flex-col bg-bd-bg-panel">
    <div class="border-b border-bd-border p-3">
      <h3 class="font-bd-sans text-xs font-semibold uppercase tracking-wider text-bd-text-muted">
        Properties
      </h3>
    </div>

    <div v-if="!selectedNode" class="flex flex-1 items-center justify-center p-4">
      <p class="text-center text-xs text-bd-text-muted">Select a node to edit properties</p>
    </div>

    <div v-else class="flex-1 overflow-y-auto p-3">
      <div class="mb-4">
        <h4 class="font-bd-sans text-sm font-semibold text-bd-chrome-mid">
          {{ selectedNode.data?.label }}
        </h4>
        <p class="text-[10px] text-bd-text-muted">{{ selectedNode.type }}</p>
      </div>

      <div v-if="nodeDef" class="space-y-3">
        <template v-for="prop in nodeDef.properties" :key="prop.key">
          <div v-if="prop.type === 'select'" class="flex flex-col gap-1">
            <label class="text-xs font-medium text-bd-text-secondary">{{ prop.label }}</label>
            <select
              :value="selectedNode.data?.properties[prop.key] ?? prop.default"
              class="w-full rounded border border-bd-border bg-bd-bg-surface px-2 py-1.5 text-xs text-bd-text-primary"
              @change="updateProperty(prop.key, ($event.target as HTMLSelectElement).value)"
            >
              <option v-for="opt in prop.options" :key="String(opt)" :value="opt">{{ opt }}</option>
            </select>
          </div>
          <div v-else-if="prop.type === 'boolean'" class="flex items-center gap-2">
            <input
              type="checkbox"
              :checked="Boolean(selectedNode.data?.properties[prop.key] ?? prop.default)"
              class="h-3.5 w-3.5 rounded border-bd-border bg-bd-bg-surface text-bd-accent"
              @change="updateProperty(prop.key, ($event.target as HTMLInputElement).checked)"
            />
            <label class="text-xs text-bd-text-secondary">{{ prop.label }}</label>
          </div>
          <BdInput
            v-else
            :model-value="String(selectedNode.data?.properties[prop.key] ?? prop.default ?? '')"
            :label="prop.label"
            :type="prop.type === 'number' ? 'number' : 'text'"
            @update:model-value="updateProperty(prop.key, prop.type === 'number' ? Number($event) : $event)"
          />
        </template>
      </div>

      <button
        class="mt-6 w-full rounded border border-bd-error/30 px-3 py-1.5 text-xs text-bd-error transition-colors hover:bg-bd-error/10"
        @click="store.removeNode(selectedNode.id)"
      >
        Delete Node
      </button>
    </div>
  </div>
</template>

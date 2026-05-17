<script setup lang="ts">
import { computed, ref } from 'vue'
import { NODE_DEFINITIONS, type NodeDefinition } from '@/types/editor'

const emit = defineEmits<{
  (e: 'add-node', def: NodeDefinition): void
}>()

const search = ref('')
const categories = ['Hardware', 'Logic', 'Timing', 'Constants'] as const

const filteredNodes = computed(() => {
  const q = search.value.toLowerCase()
  return NODE_DEFINITIONS.filter((n) => !q || n.label.toLowerCase().includes(q))
})

function nodesByCategory(cat: string) {
  return filteredNodes.value.filter((n) => n.category === cat)
}
</script>

<template>
  <div class="flex h-full flex-col bg-bd-bg-panel">
    <div class="border-b border-bd-border p-3">
      <h3 class="mb-2 font-bd-sans text-xs font-semibold uppercase tracking-wider text-bd-text-muted">
        Node Palette
      </h3>
      <input
        v-model="search"
        type="text"
        placeholder="Search nodes..."
        class="w-full rounded border border-bd-border bg-bd-bg-surface px-2 py-1.5 text-xs text-bd-text-primary placeholder-bd-text-muted focus:border-bd-border-accent focus:outline-none"
      />
    </div>
    <div class="flex-1 overflow-y-auto p-3">
      <template v-for="cat in categories" :key="cat">
        <div v-if="nodesByCategory(cat).length" class="mb-4">
          <h4 class="mb-2 font-bd-sans text-[10px] font-semibold uppercase tracking-wider text-bd-text-secondary">
            {{ cat }}
          </h4>
          <div class="space-y-1">
            <button
              v-for="def in nodesByCategory(cat)"
              :key="def.type"
              class="flex w-full items-center gap-2 rounded border border-bd-border bg-bd-bg-surface px-2 py-1.5 text-left text-xs text-bd-text-primary transition-colors hover:border-bd-border-accent hover:bg-bd-bg-secondary"
              @click="emit('add-node', def)"
            >
              <span class="h-2 w-2 rounded-full" :class="{
                'bg-bd-success': cat === 'Hardware',
                'bg-bd-accent-highlight': cat === 'Logic',
                'bg-bd-accent': cat === 'Timing',
                'bg-bd-warning': cat === 'Constants',
              }" />
              {{ def.label }}
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

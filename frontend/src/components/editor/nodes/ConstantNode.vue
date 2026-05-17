<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

defineProps<{
  data: {
    label: string
    properties: Record<string, string | number | boolean>
  }
}>()

const isTrue = (label: string) => label === 'Constant TRUE'
</script>

<template>
  <div class="min-w-[120px] rounded border border-bd-border bg-bd-bg-surface shadow-bd-node">
    <div class="rounded-t bg-gradient-to-r from-bd-chrome-dark to-bd-chrome-mid px-3 py-1.5">
      <span class="font-bd-sans text-xs font-semibold text-bd-text-primary">{{ data.label }}</span>
    </div>
    <div class="flex items-center justify-center px-3 py-3">
      <span
        class="font-bd-mono text-sm font-bold"
        :class="isTrue(data.label) ? 'text-bd-success' : 'text-bd-error'"
      >
        {{ isTrue(data.label) ? 'TRUE' : 'FALSE' }}
      </span>
    </div>
    <Handle type="source" :position="Position.Right" id="out"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface"
      :class="isTrue(data.label) ? '!bg-bd-success' : '!bg-bd-error'" />
  </div>
</template>

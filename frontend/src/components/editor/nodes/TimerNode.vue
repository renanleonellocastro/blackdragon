<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

defineProps<{
  data: {
    label: string
    properties: Record<string, string | number | boolean>
  }
}>()
</script>

<template>
  <div class="min-w-[140px] rounded border border-bd-border bg-bd-bg-surface shadow-bd-node">
    <div class="rounded-t bg-gradient-to-r from-bd-chrome-dark to-bd-chrome-mid px-3 py-1.5">
      <span class="font-bd-sans text-xs font-semibold text-bd-text-primary">{{ data.label }}</span>
    </div>
    <div class="px-3 py-2">
      <span class="font-bd-mono text-xs text-bd-text-secondary">
        {{ data.properties.duration_ms ?? 1000 }}ms
      </span>
    </div>
    <Handle type="target" :position="Position.Left" id="trigger"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface !bg-bd-accent" />
    <Handle type="source" :position="Position.Right" id="out"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface !bg-bd-success" />
  </div>
</template>

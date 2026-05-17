<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

const props = defineProps<{
  data: {
    label: string
    properties: Record<string, string | number | boolean>
    variant?: string
  }
}>()

const gateSymbol: Record<string, string> = {
  'AND Gate': '&',
  'OR Gate': '≥1',
  'NOT Gate': '1',
  'XOR Gate': '=1',
}
const hasSecondInput = props.data.label !== 'NOT Gate'
</script>

<template>
  <div class="min-w-[120px] rounded border border-bd-border bg-bd-bg-surface shadow-bd-node">
    <div class="rounded-t bg-gradient-to-r from-bd-chrome-dark to-bd-chrome-mid px-3 py-1.5">
      <span class="font-bd-sans text-xs font-semibold text-bd-text-primary">{{ data.label }}</span>
    </div>
    <div class="flex items-center justify-center px-3 py-3">
      <span class="font-bd-mono text-lg font-bold text-bd-chrome-light">
        {{ gateSymbol[data.label] || '?' }}
      </span>
    </div>
    <Handle type="target" :position="Position.Left" id="a" :style="{ top: hasSecondInput ? '35%' : '50%' }"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface !bg-bd-accent-highlight" />
    <Handle v-if="hasSecondInput" type="target" :position="Position.Left" id="b" style="top: 65%"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface !bg-bd-accent-highlight" />
    <Handle type="source" :position="Position.Right" id="out"
      class="!h-3 !w-3 !border-2 !border-bd-bg-surface !bg-bd-accent-highlight" />
  </div>
</template>

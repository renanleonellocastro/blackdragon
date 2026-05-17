<script setup lang="ts">
import type { BoardInstanceChannel } from '@/services/board.service'

defineProps<{ channels: BoardInstanceChannel[] }>()
const emit = defineEmits<{
  (e: 'update', channel: { channel_number: number; name: string; gpio_pin: number; pull_mode: string; inverted: boolean; debounce_ms: number; is_enabled: boolean }): void
}>()

function update(ch: BoardInstanceChannel, field: string, value: unknown) {
  emit('update', { ...ch, [field]: value })
}
</script>

<template>
  <div class="space-y-2">
    <div
      v-for="ch in channels"
      :key="ch.id"
      class="flex items-center gap-2 border-b border-bd-border pb-2"
    >
      <span class="w-6 text-center text-xs text-bd-text-muted">{{ ch.channel_number }}</span>
      <span
        class="w-10 text-center text-[10px] font-semibold uppercase"
        :class="ch.direction === 'input' ? 'text-bd-success' : 'text-bd-warning'"
      >
        {{ ch.direction === 'input' ? 'IN' : 'OUT' }}
      </span>
      <input
        :value="ch.name"
        class="flex-1 rounded border border-bd-border bg-bd-bg-surface px-2 py-1 text-xs text-bd-text-primary"
        @change="update(ch, 'name', ($event.target as HTMLInputElement).value)"
      />
      <input
        :value="ch.gpio_pin"
        type="number"
        class="w-14 rounded border border-bd-border bg-bd-bg-surface px-2 py-1 text-xs text-bd-text-primary"
        @change="update(ch, 'gpio_pin', Number(($event.target as HTMLInputElement).value))"
      />
      <select
        :value="ch.pull_mode"
        class="w-20 rounded border border-bd-border bg-bd-bg-surface px-1 py-1 text-xs text-bd-text-primary"
        @change="update(ch, 'pull_mode', ($event.target as HTMLSelectElement).value)"
      >
        <option value="none">None</option>
        <option value="pullup">Pull Up</option>
        <option value="pulldown">Pull Down</option>
      </select>
      <label class="flex items-center gap-1 text-xs text-bd-text-muted">
        <input
          type="checkbox"
          :checked="ch.inverted"
          class="h-3 w-3"
          @change="update(ch, 'inverted', ($event.target as HTMLInputElement).checked)"
        />
        Inv
      </label>
    </div>
  </div>
</template>

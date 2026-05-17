<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import BdButton from '@/components/ui/BdButton.vue'
import type { BoardModel } from '@/services/board.service'

defineProps<{ boards: BoardModel[] }>()
const emit = defineEmits<{ (e: 'select', board: BoardModel): void }>()
</script>

<template>
  <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
    <BdCard v-for="board in boards" :key="board.id" hoverable circuit-bg>
      <div class="p-4">
        <div class="mb-3 h-24 rounded bg-bd-bg-surface" />
        <h3 class="font-bd-sans text-sm font-semibold text-bd-chrome-light">{{ board.name }}</h3>
        <p v-if="board.description" class="mt-1 text-xs text-bd-text-secondary line-clamp-2">
          {{ board.description }}
        </p>
        <div class="mt-2 flex gap-3 text-[10px] text-bd-text-muted">
          <span>{{ board.platform }}</span>
          <span>{{ board.channels.length }} channels</span>
        </div>
        <BdButton size="sm" variant="primary" class="mt-3 w-full" @click="emit('select', board)">
          Add to Project
        </BdButton>
      </div>
    </BdCard>
  </div>
</template>

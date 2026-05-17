<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import BdButton from '@/components/ui/BdButton.vue'
import IoChannelEditor from './IoChannelEditor.vue'
import type { BoardInstance } from '@/services/board.service'
import * as boardService from '@/services/board.service'

const props = defineProps<{ instance: BoardInstance }>()
const emit = defineEmits<{ (e: 'delete'): void }>()

async function handleChannelUpdate(config: Parameters<typeof boardService.updateChannel>[1]) {
  await boardService.updateChannel(props.instance.id, config)
}
</script>

<template>
  <BdCard>
    <div class="p-4">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h3 class="font-bd-sans text-sm font-semibold text-bd-text-primary">{{ instance.name }}</h3>
          <p class="text-[10px] text-bd-text-muted font-bd-mono">{{ instance.esphome_name }}</p>
        </div>
        <BdButton size="sm" variant="danger" @click="emit('delete')">Remove</BdButton>
      </div>
      <IoChannelEditor :channels="instance.channels" @update="handleChannelUpdate" />
    </div>
  </BdCard>
</template>

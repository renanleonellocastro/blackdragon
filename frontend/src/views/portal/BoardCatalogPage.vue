<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdModal from '@/components/ui/BdModal.vue'
import BdInput from '@/components/ui/BdInput.vue'
import BoardSelector from '@/components/boards/BoardSelector.vue'
import BoardConfigurator from '@/components/boards/BoardConfigurator.vue'
import { useBoardStore } from '@/stores/board'
import { useProjectStore } from '@/stores/project'
import type { BoardModel } from '@/services/board.service'

const boardStore = useBoardStore()
const projectStore = useProjectStore()

const showAddModal = ref(false)
const selectedModel = ref<BoardModel | null>(null)
const newInstanceForm = ref({ name: '', esphome_name: '', device_address: '' })

onMounted(async () => {
  await boardStore.fetchCatalog()
  if (projectStore.currentProject) {
    await boardStore.fetchInstances(projectStore.currentProject.id)
  }
})

function selectBoard(board: BoardModel) {
  selectedModel.value = board
  showAddModal.value = true
}

async function addInstance() {
  if (!projectStore.currentProject || !selectedModel.value) return
  await boardStore.addInstance(projectStore.currentProject.id, {
    board_model_id: selectedModel.value.id,
    name: newInstanceForm.value.name,
    esphome_name: newInstanceForm.value.esphome_name,
    device_address: newInstanceForm.value.device_address || undefined,
  })
  showAddModal.value = false
  newInstanceForm.value = { name: '', esphome_name: '', device_address: '' }
}

async function removeInstance(id: string) {
  await boardStore.removeInstance(id)
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Board Configuration</h1>
    </div>

    <section class="mb-8">
      <h2 class="mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">Board Catalog</h2>
      <BoardSelector :boards="boardStore.catalog" @select="selectBoard" />
    </section>

    <section>
      <h2 class="mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">Project Boards</h2>
      <div v-if="boardStore.instances.length === 0" class="text-sm text-bd-text-muted">
        No boards added to this project yet.
      </div>
      <div v-else class="space-y-4">
        <BoardConfigurator
          v-for="inst in boardStore.instances"
          :key="inst.id"
          :instance="inst"
          @delete="removeInstance(inst.id)"
        />
      </div>
    </section>

    <BdModal :open="showAddModal" title="Add Board Instance" @close="showAddModal = false">
      <form class="space-y-4" @submit.prevent="addInstance">
        <p v-if="selectedModel" class="text-sm text-bd-text-secondary">
          Adding <strong class="text-bd-chrome-light">{{ selectedModel.name }}</strong>
        </p>
        <BdInput v-model="newInstanceForm.name" label="Board Name" placeholder="e.g. Living Room Board" />
        <BdInput v-model="newInstanceForm.esphome_name" label="ESPHome Name" placeholder="e.g. living_room" />
        <BdInput v-model="newInstanceForm.device_address" label="Device Address" placeholder="e.g. 192.168.1.100 (optional)" />
        <div class="flex justify-end gap-2 pt-2">
          <BdButton variant="secondary" @click="showAddModal = false">Cancel</BdButton>
          <BdButton type="submit" variant="primary">Add Board</BdButton>
        </div>
      </form>
    </BdModal>
  </div>
</template>

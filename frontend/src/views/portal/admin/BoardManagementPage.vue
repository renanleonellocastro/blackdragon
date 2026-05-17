<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdButton from '@/components/ui/BdButton.vue'
import { useBoardStore } from '@/stores/board'

const boardStore = useBoardStore()
const showAdd = ref(false)

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'platform', label: 'Platform' },
  { key: 'board_variant', label: 'Variant' },
  { key: 'is_active', label: 'Active' },
]

onMounted(() => boardStore.fetchCatalog())
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Board Management</h1>
      <BdButton variant="primary" @click="showAdd = true">Add Board Model</BdButton>
    </div>
    <BdTable :columns="columns" :data="boardStore.catalog">
      <template #cell-is_active="{ row }">
        {{ row.is_active ? 'Yes' : 'No' }}
      </template>
    </BdTable>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import BdModal from '@/components/ui/BdModal.vue'
import BdInput from '@/components/ui/BdInput.vue'
import { useProjectStore } from '@/stores/project'
import api from '@/services/api'
import type { PropertyType } from '@/types/project'

const projectStore = useProjectStore()
const showCreateModal = ref(false)
const properties = ref<PropertyType[]>([])
const newProject = ref({ name: '', description: '', property_id: '' })

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'status', label: 'Status', sortable: true },
  { key: 'current_version', label: 'Version' },
  { key: 'updated_at', label: 'Updated', sortable: true },
  { key: 'actions', label: '' },
]

onMounted(async () => {
  const [, propRes] = await Promise.all([
    projectStore.fetchProjects(),
    api.get<PropertyType[]>('/properties'),
  ])
  properties.value = propRes.data
})

async function handleCreate() {
  if (!newProject.value.name || !newProject.value.property_id) return
  await projectStore.createProject({
    name: newProject.value.name,
    description: newProject.value.description || undefined,
    property_id: newProject.value.property_id,
  })
  showCreateModal.value = false
  newProject.value = { name: '', description: '', property_id: '' }
}

const statusColor = (s: string) =>
  s === 'active' ? 'success' : s === 'draft' ? 'warning' : 'neutral'
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Projects</h1>
      <BdButton variant="primary" @click="showCreateModal = true">New Project</BdButton>
    </div>

    <BdTable :columns="columns" :data="projectStore.projects">
      <template #cell-status="{ row }">
        <BdStatusIndicator :status="statusColor(row.status)" variant="badge" :label="row.status" />
      </template>
      <template #cell-updated_at="{ row }">
        {{ new Date(row.updated_at).toLocaleDateString() }}
      </template>
      <template #cell-actions="{ row }">
        <div class="flex gap-2">
          <BdButton size="sm" variant="ghost" @click="$router.push(`/portal/projects/${row.id}`)">
            Open
          </BdButton>
          <BdButton size="sm" variant="ghost" @click="projectStore.duplicateProject(row.id)">
            Duplicate
          </BdButton>
        </div>
      </template>
    </BdTable>

    <BdModal :open="showCreateModal" title="New Project" @close="showCreateModal = false">
      <form class="space-y-4" @submit.prevent="handleCreate">
        <BdInput v-model="newProject.name" label="Name" placeholder="Project name" />
        <BdInput v-model="newProject.description" label="Description" placeholder="Optional" />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-bd-text-secondary">Property</label>
          <select
            v-model="newProject.property_id"
            class="w-full rounded border border-bd-border bg-bd-bg-surface px-3 py-2 text-sm text-bd-text-primary"
          >
            <option value="" disabled>Select a property</option>
            <option v-for="prop in properties" :key="prop.id" :value="prop.id">
              {{ prop.name }}
            </option>
          </select>
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <BdButton variant="secondary" @click="showCreateModal = false">Cancel</BdButton>
          <BdButton type="submit" variant="primary">Create</BdButton>
        </div>
      </form>
    </BdModal>
  </div>
</template>

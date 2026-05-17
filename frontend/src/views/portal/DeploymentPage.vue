<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import * as deploymentService from '@/services/deployment.service'
import type { DeploymentItem } from '@/services/deployment.service'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()
const deployments = ref<DeploymentItem[]>([])
const loading = ref(true)

const columns = [
  { key: 'status', label: 'Status' },
  { key: 'progress_percent', label: 'Progress' },
  { key: 'started_at', label: 'Started', sortable: true },
  { key: 'completed_at', label: 'Completed' },
  { key: 'actions', label: '' },
]

onMounted(async () => {
  if (projectStore.currentProject) {
    deployments.value = await deploymentService.listDeployments(projectStore.currentProject.id)
  }
  loading.value = false
})

const statusColor = (s: string) =>
  s === 'success' ? 'success' : s === 'failed' ? 'error' : s === 'cancelled' ? 'neutral' : 'warning'

async function cancel(id: string) {
  if (!projectStore.currentProject) return
  await deploymentService.cancelDeployment(projectStore.currentProject.id, id)
  deployments.value = await deploymentService.listDeployments(projectStore.currentProject.id)
}
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Deployments</h1>
      <p class="text-sm text-bd-text-secondary">OTA deployment history and status</p>
    </div>

    <div v-if="loading" class="text-bd-text-muted">Loading...</div>

    <div v-else-if="deployments.length === 0" class="text-bd-text-muted">
      No deployments yet. Compile a diagram and deploy to a board.
    </div>

    <BdTable v-else :columns="columns" :data="deployments">
      <template #cell-status="{ row }">
        <BdStatusIndicator :status="statusColor(row.status)" variant="badge" :label="row.status" />
      </template>
      <template #cell-progress_percent="{ row }">
        <div class="flex items-center gap-2">
          <div class="h-2 w-24 rounded-full bg-bd-bg-surface">
            <div
              class="h-2 rounded-full bg-bd-accent-highlight transition-all"
              :style="{ width: `${row.progress_percent}%` }"
            />
          </div>
          <span class="text-xs text-bd-text-muted">{{ row.progress_percent }}%</span>
        </div>
      </template>
      <template #cell-started_at="{ row }">
        {{ new Date(row.started_at).toLocaleString() }}
      </template>
      <template #cell-completed_at="{ row }">
        {{ row.completed_at ? new Date(row.completed_at).toLocaleString() : '—' }}
      </template>
      <template #cell-actions="{ row }">
        <BdButton
          v-if="row.status === 'pending' || row.status === 'uploading'"
          size="sm"
          variant="danger"
          @click="cancel(row.id)"
        >
          Cancel
        </BdButton>
      </template>
    </BdTable>
  </div>
</template>

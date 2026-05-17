<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import api from '@/services/api'

interface TenantItem {
  id: string; name: string; slug: string; is_active: boolean; created_at: string
}

const tenants = ref<TenantItem[]>([])
const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'slug', label: 'Slug' },
  { key: 'is_active', label: 'Status' },
  { key: 'created_at', label: 'Created', sortable: true },
]

onMounted(async () => {
  const { data } = await api.get<TenantItem[]>('/admin/tenants')
  tenants.value = data
})
</script>

<template>
  <div>
    <h1 class="mb-6 font-bd-sans text-2xl font-bold text-bd-text-primary">Client Management</h1>
    <BdTable :columns="columns" :data="tenants">
      <template #cell-is_active="{ row }">
        <BdStatusIndicator :status="row.is_active ? 'success' : 'error'" variant="badge" :label="row.is_active ? 'Active' : 'Inactive'" />
      </template>
      <template #cell-created_at="{ row }">
        {{ new Date(row.created_at).toLocaleDateString() }}
      </template>
    </BdTable>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import api from '@/services/api'

interface UserItem {
  id: string; email: string; full_name: string; role: string; is_active: boolean; created_at: string
}

const users = ref<UserItem[]>([])
const columns = [
  { key: 'email', label: 'Email', sortable: true },
  { key: 'full_name', label: 'Name', sortable: true },
  { key: 'role', label: 'Role' },
  { key: 'is_active', label: 'Status' },
  { key: 'actions', label: '' },
]

onMounted(async () => {
  const { data } = await api.get<UserItem[]>('/admin/users')
  users.value = data
})

async function toggleActive(user: UserItem) {
  if (user.is_active) {
    await api.post(`/admin/users/${user.id}/deactivate`)
  } else {
    await api.patch(`/admin/users/${user.id}`, { is_active: true })
  }
  const { data } = await api.get<UserItem[]>('/admin/users')
  users.value = data
}
</script>

<template>
  <div>
    <h1 class="mb-6 font-bd-sans text-2xl font-bold text-bd-text-primary">User Management</h1>
    <BdTable :columns="columns" :data="users">
      <template #cell-is_active="{ row }">
        <BdStatusIndicator :status="row.is_active ? 'success' : 'error'" variant="badge" :label="row.is_active ? 'Active' : 'Inactive'" />
      </template>
      <template #cell-actions="{ row }">
        <BdButton size="sm" :variant="row.is_active ? 'danger' : 'primary'" @click="toggleActive(row)">
          {{ row.is_active ? 'Deactivate' : 'Activate' }}
        </BdButton>
      </template>
    </BdTable>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdTable from '@/components/ui/BdTable.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdModal from '@/components/ui/BdModal.vue'
import BdInput from '@/components/ui/BdInput.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import api from '@/services/api'

interface BlogItem {
  id: string; title: string; slug: string; status: string; created_at: string
}

const posts = ref<BlogItem[]>([])
const showEditor = ref(false)
const editForm = ref({ title: '', slug: '', excerpt: '', content: '', status: 'draft' })

const columns = [
  { key: 'title', label: 'Title', sortable: true },
  { key: 'status', label: 'Status' },
  { key: 'created_at', label: 'Created', sortable: true },
  { key: 'actions', label: '' },
]

onMounted(async () => {
  // Admin blog list - uses same endpoint for now
  const { data } = await api.get<BlogItem[]>('/blog')
  posts.value = data
})

async function createPost() {
  await api.post('/blog', editForm.value)
  showEditor.value = false
  editForm.value = { title: '', slug: '', excerpt: '', content: '', status: 'draft' }
  const { data } = await api.get<BlogItem[]>('/blog')
  posts.value = data
}

const statusColor = (s: string) => s === 'published' ? 'success' : s === 'draft' ? 'warning' : 'neutral'
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Blog Management</h1>
      <BdButton variant="primary" @click="showEditor = true">New Post</BdButton>
    </div>
    <BdTable :columns="columns" :data="posts">
      <template #cell-status="{ row }">
        <BdStatusIndicator :status="statusColor(row.status)" variant="badge" :label="row.status" />
      </template>
      <template #cell-created_at="{ row }">
        {{ new Date(row.created_at).toLocaleDateString() }}
      </template>
    </BdTable>

    <BdModal :open="showEditor" title="New Blog Post" @close="showEditor = false">
      <form class="space-y-4" @submit.prevent="createPost">
        <BdInput v-model="editForm.title" label="Title" />
        <BdInput v-model="editForm.slug" label="Slug" />
        <BdInput v-model="editForm.excerpt" label="Excerpt" />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-bd-text-secondary">Content</label>
          <textarea
            v-model="editForm.content"
            rows="8"
            class="w-full rounded border border-bd-border bg-bd-bg-surface px-3 py-2 font-bd-mono text-sm text-bd-text-primary"
          />
        </div>
        <div class="flex justify-end gap-2">
          <BdButton variant="secondary" @click="showEditor = false">Cancel</BdButton>
          <BdButton type="submit" variant="primary">Create</BdButton>
        </div>
      </form>
    </BdModal>
  </div>
</template>

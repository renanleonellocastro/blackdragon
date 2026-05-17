<script setup lang="ts">
import { computed } from 'vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
  class?: string
}

interface Props {
  columns: Column[]
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any[]
  sortBy?: string
  sortDir?: 'asc' | 'desc'
}

const props = withDefaults(defineProps<Props>(), {
  sortBy: '',
  sortDir: 'asc',
})

const emit = defineEmits<{
  sort: [key: string]
}>()

const sortedData = computed(() => {
  if (!props.sortBy) return props.data
  return [...props.data].sort((a, b) => {
    const aVal = String(a[props.sortBy] ?? '')
    const bVal = String(b[props.sortBy] ?? '')
    const cmp = aVal.localeCompare(bVal)
    return props.sortDir === 'asc' ? cmp : -cmp
  })
})
</script>

<template>
  <div class="overflow-x-auto rounded-lg border border-bd-border">
    <table class="w-full text-left text-sm">
      <thead class="bg-bd-bg-panel text-bd-text-secondary">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-3 font-medium"
            :class="[col.class, col.sortable && 'cursor-pointer select-none hover:text-bd-text-primary']"
            @click="col.sortable && emit('sort', col.key)"
          >
            <span class="inline-flex items-center gap-1">
              {{ col.label }}
              <template v-if="col.sortable && sortBy === col.key">
                <svg v-if="sortDir === 'asc'" class="h-3 w-3" viewBox="0 0 12 12" fill="currentColor"><path d="M6 2l4 5H2z"/></svg>
                <svg v-else class="h-3 w-3" viewBox="0 0 12 12" fill="currentColor"><path d="M6 10L2 5h8z"/></svg>
              </template>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, i) in sortedData"
          :key="i"
          class="border-t border-bd-border transition-colors hover:bg-bd-bg-surface"
          :class="i % 2 === 0 ? 'bg-bd-bg-primary' : 'bg-bd-bg-secondary'"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-3 text-bd-text-primary"
            :class="col.class"
          >
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
        <tr v-if="sortedData.length === 0">
          <td :colspan="columns.length" class="px-4 py-8 text-center text-bd-text-muted">
            No data available
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

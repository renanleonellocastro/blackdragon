import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BoardModel, BoardInstance } from '@/services/board.service'
import * as boardService from '@/services/board.service'

export const useBoardStore = defineStore('board', () => {
  const catalog = ref<BoardModel[]>([])
  const instances = ref<BoardInstance[]>([])
  const loading = ref(false)

  async function fetchCatalog() {
    loading.value = true
    try {
      catalog.value = await boardService.listCatalog()
    } finally {
      loading.value = false
    }
  }

  async function fetchInstances(projectId: string) {
    loading.value = true
    try {
      instances.value = await boardService.listInstances(projectId)
    } finally {
      loading.value = false
    }
  }

  async function addInstance(projectId: string, payload: Parameters<typeof boardService.createInstance>[1]) {
    const instance = await boardService.createInstance(projectId, payload)
    instances.value.push(instance)
    return instance
  }

  async function removeInstance(instanceId: string) {
    await boardService.deleteInstance(instanceId)
    instances.value = instances.value.filter((i) => i.id !== instanceId)
  }

  return { catalog, instances, loading, fetchCatalog, fetchInstances, addInstance, removeInstance }
})

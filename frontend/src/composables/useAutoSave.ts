import { onUnmounted, ref } from 'vue'
import { useEditorStore } from '@/stores/editor'
import api from '@/services/api'

export function useAutoSave(projectId: string) {
  const store = useEditorStore()
  const lastSaved = ref<Date | null>(null)
  let timer: ReturnType<typeof setInterval> | null = null

  async function saveDraft() {
    if (!store.diagramId || !store.isDirty) return
    try {
      await api.post(`/projects/${projectId}/diagrams/${store.diagramId}/draft`, {
        draft_data: store.getGraphData(),
      })
      lastSaved.value = new Date()
    } catch {
      // Silent fail for auto-save
    }
  }

  timer = setInterval(saveDraft, 60_000)

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

  return { lastSaved, saveDraft }
}

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import BdButton from '@/components/ui/BdButton.vue'
import BdCard from '@/components/ui/BdCard.vue'
import * as compilerService from '@/services/compiler.service'

const route = useRoute()
const artifactId = route.params.id as string

const artifact = ref<compilerService.ArtifactResponse | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    artifact.value = await compilerService.getArtifact(artifactId)
  } finally {
    loading.value = false
  }
})

function download() {
  window.open(compilerService.getDownloadUrl(artifactId), '_blank')
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">YAML Preview</h1>
      <BdButton v-if="artifact" variant="primary" @click="download">Download YAML</BdButton>
    </div>

    <div v-if="loading" class="text-bd-text-muted">Loading...</div>

    <BdCard v-else-if="artifact">
      <div class="p-4">
        <div class="mb-4 flex gap-4 text-xs text-bd-text-muted">
          <span>Target: {{ artifact.target }}</span>
          <span>Nodes: {{ artifact.node_count }}</span>
          <span>Edges: {{ artifact.edge_count }}</span>
          <span>v{{ artifact.version }}</span>
        </div>
        <div class="relative rounded bg-bd-bg-primary p-4">
          <pre class="overflow-x-auto font-bd-mono text-sm leading-relaxed text-bd-text-primary"><code>{{ artifact.output }}</code></pre>
        </div>
      </div>
    </BdCard>
  </div>
</template>

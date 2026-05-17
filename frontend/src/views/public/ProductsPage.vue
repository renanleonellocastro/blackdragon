<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import BdTable from '@/components/ui/BdTable.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const boards = [
  { name: 'BD-IO-8', inputs: 4, outputs: 4, platform: 'ESP32', desc: 'Compact 8-channel I/O board for small installations.' },
  { name: 'BD-IO-16', inputs: 8, outputs: 8, platform: 'ESP32', desc: 'Standard 16-channel board for residential automation.' },
  { name: 'BD-IO-32', inputs: 16, outputs: 16, platform: 'ESP32-S3', desc: 'High-density 32-channel board for commercial use.' },
]

const specColumns = [
  { key: 'name', label: 'Model', sortable: true },
  { key: 'inputs', label: 'Inputs', sortable: true },
  { key: 'outputs', label: 'Outputs', sortable: true },
  { key: 'platform', label: 'Platform' },
]
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          Products
        </h1>
        <p class="mt-4 text-lg text-bd-text-secondary">
          Purpose-built ESP32-based I/O boards for smart home automation.
        </p>
      </div>
    </section>

    <section class="bg-bd-bg-secondary py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <BdCard v-for="board in boards" :key="board.name" hoverable circuit-bg>
            <div class="p-6">
              <div class="mb-4 h-32 rounded bg-bd-bg-surface" />
              <h3 class="font-bd-sans text-lg font-semibold text-bd-chrome-light">{{ board.name }}</h3>
              <p class="mt-2 text-sm text-bd-text-secondary">{{ board.desc }}</p>
              <div class="mt-4 flex gap-4 text-xs text-bd-text-muted">
                <span>{{ board.inputs }} inputs</span>
                <span>{{ board.outputs }} outputs</span>
                <span>{{ board.platform }}</span>
              </div>
            </div>
          </BdCard>
        </div>

        <div class="mt-12">
          <h2 class="mb-4 font-bd-sans text-2xl font-bold text-bd-text-primary">Specifications</h2>
          <BdTable :columns="specColumns" :data="boards" />
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

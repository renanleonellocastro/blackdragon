<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const projects = [
  { title: 'Smart Villa', scope: 'Residential', hardware: '4x BD-IO-16', outcome: 'Full home automation with 64 I/O points.' },
  { title: 'Office Complex', scope: 'Commercial', hardware: '8x BD-IO-32', outcome: 'Lighting, HVAC, and access control for 3 floors.' },
  { title: 'Greenhouse Array', scope: 'Agricultural', hardware: '12x BD-IO-8', outcome: 'Climate monitoring and irrigation for 6 greenhouses.' },
]
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          Projects
        </h1>
        <p class="mt-4 text-lg text-bd-text-secondary">
          Real-world deployments showcasing BlackDragon capabilities.
        </p>
      </div>
    </section>

    <section class="bg-bd-bg-secondary py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <BdCard v-for="proj in projects" :key="proj.title" hoverable>
            <div class="p-6">
              <h3 class="font-bd-sans text-lg font-semibold text-bd-text-primary">{{ proj.title }}</h3>
              <div class="mt-3 space-y-2 text-sm">
                <div class="flex justify-between border-b border-bd-border pb-1">
                  <span class="text-bd-text-muted">Scope</span>
                  <span class="text-bd-text-secondary">{{ proj.scope }}</span>
                </div>
                <div class="flex justify-between border-b border-bd-border pb-1">
                  <span class="text-bd-text-muted">Hardware</span>
                  <span class="text-bd-text-secondary">{{ proj.hardware }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-bd-text-muted">Outcome</span>
                  <span class="text-bd-text-secondary">{{ proj.outcome }}</span>
                </div>
              </div>
            </div>
          </BdCard>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const solutions = [
  { title: 'Residential Automation', desc: 'Complete home automation with lighting, HVAC, security, and energy management.' },
  { title: 'Commercial Buildings', desc: 'Scalable automation for offices, warehouses, and retail spaces.' },
  { title: 'Agricultural IoT', desc: 'Greenhouse monitoring, irrigation control, and environmental sensors.' },
  { title: 'Industrial Monitoring', desc: 'Equipment monitoring, alert systems, and process automation.' },
]
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          Solutions
        </h1>
        <p class="mt-4 text-lg text-bd-text-secondary">
          BlackDragon powers automation across industries.
        </p>
      </div>
    </section>

    <section class="relative bg-bd-bg-secondary py-16">
      <BdCircuitPattern :opacity="0.06" />
      <div class="relative mx-auto max-w-7xl px-4 sm:px-6">
        <div class="grid gap-6 sm:grid-cols-2">
          <BdCard v-for="sol in solutions" :key="sol.title" hoverable>
            <div class="p-6">
              <h3 class="font-bd-sans text-lg font-semibold text-bd-text-primary">{{ sol.title }}</h3>
              <p class="mt-2 text-bd-text-secondary">{{ sol.desc }}</p>
            </div>
          </BdCard>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

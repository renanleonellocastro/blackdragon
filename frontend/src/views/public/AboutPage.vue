<script setup lang="ts">
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="relative py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          About BlackDragon
        </h1>
        <p class="mt-4 max-w-3xl text-lg text-bd-text-secondary">
          BlackDragon delivers industrial-grade smart home automation through purpose-built
          ESP32-based I/O boards and an intuitive visual programming environment.
        </p>
      </div>
    </section>

    <section class="relative bg-bd-bg-secondary py-16">
      <BdCircuitPattern :opacity="0.08" />
      <div class="relative mx-auto max-w-7xl px-4 sm:px-6">
        <h2 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Our Mission</h2>
        <p class="mt-4 max-w-3xl text-bd-text-secondary">
          Empowering homeowners and integrators with professional-grade automation tools
          that bridge the gap between hardware engineering and intuitive software design.
        </p>
      </div>
    </section>

    <section class="py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h2 class="font-bd-sans text-2xl font-bold text-bd-text-primary">The Team</h2>
        <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <BdCard v-for="i in 3" :key="i" hoverable>
            <div class="p-6 text-center">
              <div class="mx-auto h-16 w-16 rounded-full bg-bd-bg-surface" />
              <h3 class="mt-4 font-bd-sans font-semibold text-bd-text-primary">Team Member</h3>
              <p class="text-sm text-bd-text-secondary">Engineering</p>
            </div>
          </BdCard>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

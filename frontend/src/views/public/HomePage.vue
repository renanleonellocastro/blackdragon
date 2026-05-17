<script setup lang="ts">
import BdLogo from '@/components/ui/BdLogo.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const features = [
  { title: 'Visual Programming', desc: 'Drag-and-drop blocks-and-wires editor for intuitive automation design.' },
  { title: 'ESP32 Compilation', desc: 'Generate production-ready ESPHome YAML from visual diagrams.' },
  { title: 'OTA Deployment', desc: 'Push configurations to your boards over-the-air with one click.' },
  { title: 'Multi-Tenant Portal', desc: 'Secure client portal with project management and version control.' },
]
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <!-- Hero -->
    <section class="relative overflow-hidden bg-bd-hero py-24 sm:py-32">
      <BdCircuitPattern :opacity="0.1" />
      <div class="relative mx-auto max-w-7xl px-4 text-center sm:px-6">
        <BdLogo size="xl" class="mx-auto mb-6" />
        <h1 class="font-bd-sans text-4xl font-bold text-bd-text-primary sm:text-6xl">
          BlackDragon
        </h1>
        <p class="mx-auto mt-4 max-w-2xl text-lg text-bd-text-secondary">
          Industrial-grade smart home automation. Design, compile, and deploy ESP32 firmware
          through an intuitive visual programming environment.
        </p>
        <div class="mt-8 flex justify-center gap-4">
          <BdButton size="lg" variant="primary" @click="$router.push('/register')">
            Get Started
          </BdButton>
          <BdButton size="lg" variant="secondary" @click="$router.push('/products')">
            View Products
          </BdButton>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-bd-bg-secondary py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h2 class="text-center font-bd-sans text-3xl font-bold text-bd-text-primary">
          Platform Capabilities
        </h2>
        <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <BdCard v-for="feature in features" :key="feature.title" hoverable circuit-bg>
            <div class="p-6">
              <h3 class="font-bd-sans text-lg font-semibold text-bd-text-primary">
                {{ feature.title }}
              </h3>
              <p class="mt-2 text-sm text-bd-text-secondary">{{ feature.desc }}</p>
            </div>
          </BdCard>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

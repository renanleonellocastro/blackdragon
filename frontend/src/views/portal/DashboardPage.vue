<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdLogo from '@/components/ui/BdLogo.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import { useProjectStore } from '@/stores/project'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import type { PropertyType } from '@/types/project'

const projectStore = useProjectStore()
const authStore = useAuthStore()

const properties = ref<PropertyType[]>([])

onMounted(async () => {
  const [, propRes] = await Promise.all([
    projectStore.fetchProjects(),
    api.get<PropertyType[]>('/properties'),
  ])
  properties.value = propRes.data
})

const statusColor = (s: string) =>
  s === 'active' ? 'success' : s === 'draft' ? 'warning' : 'neutral'
</script>

<template>
  <div>
    <div class="mb-8 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <BdLogo size="md" />
        <div>
          <h1 class="font-bd-sans text-2xl font-bold text-bd-text-primary">Dashboard</h1>
          <p class="text-sm text-bd-text-secondary">
            Welcome back, {{ authStore.user?.full_name }}
          </p>
        </div>
      </div>
      <BdButton variant="primary" @click="$router.push('/portal/projects')">
        View Projects
      </BdButton>
    </div>

    <!-- Properties -->
    <section class="mb-8">
      <h2 class="mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">Properties</h2>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <BdCard v-for="prop in properties" :key="prop.id" hoverable>
          <div class="p-4">
            <h3 class="font-bd-sans font-semibold text-bd-text-primary">{{ prop.name }}</h3>
            <p v-if="prop.address" class="mt-1 text-xs text-bd-text-muted">{{ prop.address }}</p>
          </div>
        </BdCard>
      </div>
    </section>

    <!-- Recent Projects -->
    <section class="relative">
      <BdCircuitPattern :opacity="0.04" />
      <h2 class="relative mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">
        Recent Projects
      </h2>
      <div class="relative grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <BdCard
          v-for="proj in projectStore.projects.slice(0, 6)"
          :key="proj.id"
          hoverable
          class="cursor-pointer"
          @click="$router.push(`/portal/projects/${proj.id}`)"
        >
          <div class="p-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bd-sans font-semibold text-bd-text-primary">{{ proj.name }}</h3>
              <BdStatusIndicator :status="statusColor(proj.status)" variant="badge" :label="proj.status" />
            </div>
            <p v-if="proj.description" class="mt-2 text-sm text-bd-text-secondary line-clamp-2">
              {{ proj.description }}
            </p>
            <p class="mt-3 text-xs text-bd-text-muted">v{{ proj.current_version }}</p>
          </div>
        </BdCard>
      </div>
    </section>
  </div>
</template>

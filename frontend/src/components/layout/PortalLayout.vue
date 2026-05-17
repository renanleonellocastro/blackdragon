<script setup lang="ts">
import AppSidebar from './AppSidebar.vue'
</script>

<template>
  <div class="flex h-screen bg-bd-bg-primary">
    <AppSidebar />
    <main class="flex-1 overflow-y-auto">
      <div class="px-6 py-6">
        <slot name="breadcrumb" />
        <slot />
      </div>
    </main>
  </div>
</template>

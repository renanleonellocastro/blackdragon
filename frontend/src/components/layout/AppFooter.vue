<script setup lang="ts">
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
</script>

<template>
  <footer class="relative border-t border-bd-border bg-bd-bg-secondary">
    <BdCircuitPattern :opacity="0.08" />
    <div class="relative mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
        <p class="text-sm text-bd-text-muted">
          &copy; {{ new Date().getFullYear() }} BlackDragon. All rights reserved.
        </p>
        <nav class="flex gap-6">
          <a href="/about" class="text-sm text-bd-text-muted transition-colors hover:text-bd-text-secondary">About</a>
          <a href="/contact" class="text-sm text-bd-text-muted transition-colors hover:text-bd-text-secondary">Contact</a>
        </nav>
      </div>
    </div>
  </footer>
</template>

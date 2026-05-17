<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import BdLogo from '@/components/ui/BdLogo.vue'

const mobileMenuOpen = ref(false)

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/products', label: 'Products' },
  { to: '/solutions', label: 'Solutions' },
  { to: '/projects', label: 'Projects' },
  { to: '/blog', label: 'Blog' },
  { to: '/contact', label: 'Contact' },
]
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-bd-chrome-dark bg-bd-bg-primary/95 backdrop-blur-sm">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
      <RouterLink to="/" class="flex items-center gap-2">
        <BdLogo size="md" />
        <span class="font-bd-sans text-lg font-semibold text-bd-text-primary">BlackDragon</span>
      </RouterLink>

      <!-- Desktop nav -->
      <nav class="hidden items-center gap-6 md:flex">
        <RouterLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="font-bd-sans text-sm text-bd-text-secondary transition-colors hover:text-bd-text-primary"
          active-class="text-bd-text-primary"
        >
          {{ link.label }}
        </RouterLink>
        <RouterLink
          to="/login"
          class="rounded border border-bd-chrome-dark bg-bd-metallic px-4 py-1.5 font-bd-sans text-sm font-medium text-bd-text-primary shadow-bd-emboss transition-shadow hover:shadow-bd-glow"
        >
          Sign In
        </RouterLink>
      </nav>

      <!-- Mobile menu button -->
      <button
        class="text-bd-text-secondary md:hidden"
        aria-label="Toggle menu"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
          <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Mobile nav -->
    <Transition name="slide-down">
      <nav v-if="mobileMenuOpen" class="border-t border-bd-border bg-bd-bg-panel px-4 py-4 md:hidden">
        <div class="flex flex-col gap-3">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="font-bd-sans text-sm text-bd-text-secondary transition-colors hover:text-bd-text-primary"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </RouterLink>
          <RouterLink
            to="/login"
            class="mt-2 rounded border border-bd-chrome-dark bg-bd-metallic px-4 py-2 text-center font-bd-sans text-sm font-medium text-bd-text-primary shadow-bd-emboss"
            @click="mobileMenuOpen = false"
          >
            Sign In
          </RouterLink>
        </div>
      </nav>
    </Transition>
  </header>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>

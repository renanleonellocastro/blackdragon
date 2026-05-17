<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const collapsed = ref(false)

interface NavItem {
  to: string
  label: string
  icon: string
}

const navItems: NavItem[] = [
  { to: '/portal', label: 'Dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { to: '/portal/projects', label: 'Projects', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
  { to: '/portal/boards', label: 'Boards', icon: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z' },
  { to: '/portal/deployments', label: 'Deploy', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' },
  { to: '/portal/profile', label: 'Profile', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' },
]
</script>

<template>
  <aside
    class="flex flex-col border-r border-bd-border bg-bd-bg-panel transition-all duration-200"
    :class="collapsed ? 'w-16' : 'w-56'"
  >
    <div class="flex h-12 items-center justify-end px-3">
      <button
        class="text-bd-text-muted transition-colors hover:text-bd-text-primary"
        aria-label="Toggle sidebar"
        @click="collapsed = !collapsed"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" :d="collapsed ? 'M13 5l7 7-7 7' : 'M11 19l-7-7 7-7'" />
        </svg>
      </button>
    </div>

    <nav class="flex-1 px-2 py-2">
      <RouterLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="mb-1 flex items-center gap-3 rounded-md px-3 py-2.5 text-sm text-bd-text-secondary transition-all hover:bg-bd-bg-surface hover:text-bd-text-primary"
        :class="[
          route.path === item.to && 'border-l-2 border-bd-accent-highlight bg-bd-bg-surface text-bd-text-primary',
        ]"
      >
        <svg class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" :d="item.icon" />
        </svg>
        <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup lang="ts">
interface Props {
  status: 'success' | 'warning' | 'error' | 'neutral'
  variant?: 'dot' | 'badge'
  label?: string
}

withDefaults(defineProps<Props>(), {
  variant: 'dot',
  label: '',
})

const colorMap = {
  success: 'bg-bd-success',
  warning: 'bg-bd-warning',
  error: 'bg-bd-error',
  neutral: 'bg-bd-accent',
} as const

const textColorMap = {
  success: 'text-bd-success',
  warning: 'text-bd-warning',
  error: 'text-bd-error',
  neutral: 'text-bd-accent',
} as const

const badgeBgMap = {
  success: 'bg-bd-success/10 border-bd-success/30',
  warning: 'bg-bd-warning/10 border-bd-warning/30',
  error: 'bg-bd-error/10 border-bd-error/30',
  neutral: 'bg-bd-accent/10 border-bd-accent/30',
} as const
</script>

<template>
  <span v-if="variant === 'dot'" class="inline-flex items-center gap-2">
    <span class="relative flex h-2.5 w-2.5">
      <span
        class="absolute inline-flex h-full w-full animate-ping rounded-full opacity-40"
        :class="colorMap[status]"
      />
      <span class="relative inline-flex h-2.5 w-2.5 rounded-full" :class="colorMap[status]" />
    </span>
    <span v-if="label" class="text-sm" :class="textColorMap[status]">{{ label }}</span>
  </span>
  <span
    v-else
    class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium"
    :class="[badgeBgMap[status], textColorMap[status]]"
  >
    <span class="h-1.5 w-1.5 rounded-full" :class="colorMap[status]" />
    <slot>{{ label }}</slot>
  </span>
</template>

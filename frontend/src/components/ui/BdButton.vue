<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  type: 'button',
})

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center rounded border font-bd-sans font-medium transition-all duration-200 focus:outline-none focus:ring-1"
    :class="[
      // Size
      {
        'px-3 py-1.5 text-sm': size === 'sm',
        'px-4 py-2 text-sm': size === 'md',
        'px-6 py-3 text-base': size === 'lg',
      },
      // Variant
      {
        'border-bd-chrome-dark bg-bd-metallic text-bd-text-primary shadow-bd-emboss hover:shadow-bd-glow focus:ring-bd-chrome-mid':
          variant === 'primary',
        'border-bd-border bg-bd-bg-surface text-bd-text-secondary hover:border-bd-border-accent hover:text-bd-text-primary hover:shadow-bd-glow focus:ring-bd-border-accent':
          variant === 'secondary',
        'border-transparent bg-transparent text-bd-text-secondary hover:text-bd-text-primary hover:bg-bd-bg-surface focus:ring-bd-border-accent':
          variant === 'ghost',
        'border-bd-error/50 bg-bd-error/10 text-bd-error hover:bg-bd-error/20 hover:shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:ring-bd-error':
          variant === 'danger',
      },
      // Disabled
      disabled && 'cursor-not-allowed opacity-50',
    ]"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

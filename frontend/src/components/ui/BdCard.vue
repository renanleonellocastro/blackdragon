<script setup lang="ts">
interface Props {
  hoverable?: boolean
  circuitBg?: boolean
}

withDefaults(defineProps<Props>(), {
  hoverable: false,
  circuitBg: false,
})
</script>

<template>
  <div
    class="relative overflow-hidden rounded-lg border border-bd-border bg-bd-bg-panel shadow-bd-emboss"
    :class="[
      hoverable && 'transition-shadow duration-200 hover:shadow-bd-glow hover:border-bd-border-accent',
    ]"
  >
    <div
      v-if="circuitBg"
      class="pointer-events-none absolute inset-0 opacity-[0.06]"
      aria-hidden="true"
      style="background-image: url('/circuit-pattern.svg'); background-repeat: repeat; background-size: 100px 100px"
    />
    <div class="relative">
      <slot />
    </div>
  </div>
</template>

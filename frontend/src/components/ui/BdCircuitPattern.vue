<script setup lang="ts">
interface Props {
  opacity?: number
  class?: string
}

withDefaults(defineProps<Props>(), {
  opacity: 0.15,
})
</script>

<template>
  <div
    class="pointer-events-none absolute inset-0 overflow-hidden"
    :class="$props.class"
    :style="{ opacity }"
    aria-hidden="true"
  >
    <div
      class="h-full w-full"
      style="background-image: url('/circuit-pattern.svg'); background-repeat: repeat; background-size: 100px 100px"
    />
  </div>
</template>

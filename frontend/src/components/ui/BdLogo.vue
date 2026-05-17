<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const sizeMap = {
  sm: 'h-6 w-6',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
  xl: 'h-20 w-20',
} as const
</script>

<template>
  <img
    src="/logo.svg"
    alt="BlackDragon"
    :class="sizeMap[props.size]"
    class="inline-block"
  />
</template>

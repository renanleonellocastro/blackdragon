<script setup lang="ts">
interface Props {
  modelValue?: string
  type?: string
  placeholder?: string
  label?: string
  error?: string
  disabled?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  type: 'text',
  placeholder: '',
  label: '',
  error: '',
  disabled: false,
  id: '',
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <label
      v-if="label"
      :for="props.id"
      class="text-sm font-medium text-bd-text-secondary"
    >
      {{ label }}
    </label>
    <input
      :id="props.id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      class="w-full rounded border bg-bd-bg-surface px-3 py-2 font-bd-sans text-sm text-bd-text-primary placeholder-bd-text-muted transition-all duration-200 focus:outline-none focus:ring-1"
      :class="[
        error
          ? 'border-bd-error focus:border-bd-error focus:ring-bd-error/50'
          : 'border-bd-border focus:border-bd-border-accent focus:shadow-bd-glow focus:ring-bd-border-accent',
        disabled && 'cursor-not-allowed opacity-50',
      ]"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="text-xs text-bd-error">{{ error }}</p>
  </div>
</template>

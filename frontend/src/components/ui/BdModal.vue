<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

interface Props {
  title?: string
  modelValue?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  modelValue: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  close: []
}>()

const modalRef = ref<HTMLDivElement | null>(null)

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') close()

  // Focus trap
  if (e.key === 'Tab' && modalRef.value) {
    const focusable = modalRef.value.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    )
    const first = focusable[0]
    const last = focusable[focusable.length - 1]
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault()
      last?.focus()
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault()
      first?.focus()
    }
  }
}

onMounted(() => document.addEventListener('keydown', handleKeydown))
onUnmounted(() => document.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <Teleport to="body">
    <Transition name="bd-modal">
      <div
        v-if="props.modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-bd-bg-primary/80 backdrop-blur-sm"
        @click.self="close"
      >
        <div
          ref="modalRef"
          class="relative mx-4 w-full max-w-lg rounded-lg border border-bd-border bg-bd-bg-panel shadow-bd-emboss"
          role="dialog"
          aria-modal="true"
        >
          <div
            v-if="title"
            class="flex items-center justify-between border-b border-bd-border px-6 py-4"
          >
            <h2 class="font-bd-sans text-lg font-semibold text-bd-text-primary">
              {{ title }}
            </h2>
            <button
              class="text-bd-text-muted transition-colors hover:text-bd-text-primary"
              aria-label="Close"
              @click="close"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="px-6 py-4">
            <slot />
          </div>
          <div v-if="$slots.footer" class="border-t border-bd-border px-6 py-4">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.bd-modal-enter-active,
.bd-modal-leave-active {
  transition: opacity 0.2s ease;
}
.bd-modal-enter-from,
.bd-modal-leave-to {
  opacity: 0;
}
</style>

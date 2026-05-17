<script setup lang="ts">
import { ref } from 'vue'
import BdInput from '@/components/ui/BdInput.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import BdStatusIndicator from '@/components/ui/BdStatusIndicator.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import api from '@/services/api'

const form = ref({ name: '', email: '', company: '', phone: '', message: '' })
const errors = ref<Record<string, string>>({})
const submitting = ref(false)
const submitted = ref(false)
const submitError = ref('')

function validate(): boolean {
  errors.value = {}
  if (!form.value.name.trim()) errors.value.name = 'Name is required'
  if (!form.value.email.trim()) errors.value.email = 'Email is required'
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) errors.value.email = 'Invalid email'
  if (!form.value.message.trim()) errors.value.message = 'Message is required'
  else if (form.value.message.trim().length < 10) errors.value.message = 'Message must be at least 10 characters'
  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return
  submitting.value = true
  submitError.value = ''
  try {
    await api.post('/leads', form.value)
    submitted.value = true
  } catch {
    submitError.value = 'Failed to submit. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="relative py-20">
      <BdCircuitPattern :opacity="0.06" />
      <div class="relative mx-auto max-w-2xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          Contact Us
        </h1>
        <p class="mt-4 text-lg text-bd-text-secondary">
          Get in touch to learn more about BlackDragon automation solutions.
        </p>

        <div v-if="submitted" class="mt-12 rounded-lg border border-bd-border bg-bd-bg-panel p-8 text-center">
          <BdStatusIndicator status="success" variant="badge" label="Submitted" />
          <p class="mt-4 text-bd-text-primary">
            Thank you for reaching out! We'll get back to you soon.
          </p>
        </div>

        <form v-else class="mt-12 space-y-6" @submit.prevent="handleSubmit">
          <div class="grid gap-6 sm:grid-cols-2">
            <BdInput
              v-model="form.name"
              label="Name"
              placeholder="Your name"
              :error="errors.name"
            />
            <BdInput
              v-model="form.email"
              type="email"
              label="Email"
              placeholder="you@company.com"
              :error="errors.email"
            />
          </div>
          <div class="grid gap-6 sm:grid-cols-2">
            <BdInput v-model="form.company" label="Company" placeholder="Optional" />
            <BdInput v-model="form.phone" label="Phone" placeholder="Optional" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-bd-text-secondary">Message</label>
            <textarea
              v-model="form.message"
              rows="5"
              placeholder="Tell us about your automation needs..."
              class="w-full rounded border border-bd-border bg-bd-bg-surface px-3 py-2 font-bd-sans text-sm text-bd-text-primary placeholder-bd-text-muted transition-all focus:border-bd-border-accent focus:shadow-bd-glow focus:outline-none focus:ring-1 focus:ring-bd-border-accent"
              :class="errors.message && 'border-bd-error focus:border-bd-error focus:ring-bd-error/50'"
            />
            <p v-if="errors.message" class="text-xs text-bd-error">{{ errors.message }}</p>
          </div>

          <p v-if="submitError" class="text-sm text-bd-error">{{ submitError }}</p>

          <BdButton type="submit" variant="primary" size="lg" :disabled="submitting">
            {{ submitting ? 'Sending...' : 'Send Message' }}
          </BdButton>
        </form>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BdLogo from '@/components/ui/BdLogo.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdInput from '@/components/ui/BdInput.vue'
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import { useAuth } from '@/composables/useAuth'

const { register } = useAuth()

const form = ref({ email: '', password: '', full_name: '', company_name: '' })
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await register({
      email: form.value.email,
      password: form.value.password,
      full_name: form.value.full_name,
      company_name: form.value.company_name || undefined,
    })
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="relative flex min-h-screen items-center justify-center bg-bd-bg-primary">
    <BdCircuitPattern :opacity="0.06" />
    <div class="relative z-10 w-full max-w-md px-4">
      <div class="mb-8 text-center">
        <BdLogo size="lg" class="mx-auto" />
        <h1 class="mt-4 font-bd-sans text-2xl font-bold text-bd-text-primary">Create Account</h1>
        <p class="mt-1 text-sm text-bd-text-secondary">Get started with BlackDragon</p>
      </div>

      <BdCard>
        <form class="space-y-6 p-6" @submit.prevent="handleSubmit">
          <BdInput v-model="form.full_name" label="Full Name" placeholder="Your name" />
          <BdInput v-model="form.email" type="email" label="Email" placeholder="you@company.com" />
          <BdInput v-model="form.password" type="password" label="Password" placeholder="Min. 8 characters" />
          <BdInput v-model="form.company_name" label="Company" placeholder="Optional" />

          <p v-if="error" class="text-sm text-bd-error">{{ error }}</p>

          <BdButton type="submit" variant="primary" size="lg" class="w-full" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Account' }}
          </BdButton>

          <p class="text-center text-sm text-bd-text-muted">
            Already have an account?
            <router-link to="/login" class="text-bd-accent-highlight hover:underline">
              Sign In
            </router-link>
          </p>
        </form>
      </BdCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BdLogo from '@/components/ui/BdLogo.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdInput from '@/components/ui/BdInput.vue'
import BdCard from '@/components/ui/BdCard.vue'
import BdCircuitPattern from '@/components/ui/BdCircuitPattern.vue'
import { useAuth } from '@/composables/useAuth'

const { login } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await login({ email: email.value, password: password.value })
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Invalid credentials'
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
        <h1 class="mt-4 font-bd-sans text-2xl font-bold text-bd-text-primary">Sign In</h1>
        <p class="mt-1 text-sm text-bd-text-secondary">Welcome back to BlackDragon</p>
      </div>

      <BdCard>
        <form class="space-y-6 p-6" @submit.prevent="handleSubmit">
          <BdInput
            v-model="email"
            type="email"
            label="Email"
            placeholder="you@company.com"
          />
          <BdInput
            v-model="password"
            type="password"
            label="Password"
            placeholder="••••••••"
          />

          <p v-if="error" class="text-sm text-bd-error">{{ error }}</p>

          <BdButton type="submit" variant="primary" size="lg" class="w-full" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </BdButton>

          <p class="text-center text-sm text-bd-text-muted">
            Don't have an account?
            <router-link to="/register" class="text-bd-accent-highlight hover:underline">
              Register
            </router-link>
          </p>
        </form>
      </BdCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BdCard from '@/components/ui/BdCard.vue'
import BdButton from '@/components/ui/BdButton.vue'
import BdInput from '@/components/ui/BdInput.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const passwordForm = ref({ current: '', new: '', confirm: '' })
const message = ref('')

async function changePassword() {
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    message.value = 'Passwords do not match'
    return
  }
  // TODO: Implement password change API
  message.value = 'Password change not yet implemented'
}
</script>

<template>
  <div>
    <h1 class="mb-6 font-bd-sans text-2xl font-bold text-bd-text-primary">Profile</h1>

    <BdCard class="mb-6">
      <div class="p-6">
        <h2 class="mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">Account Info</h2>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-bd-text-muted">Name</span>
            <span class="text-bd-text-primary">{{ auth.user?.full_name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-bd-text-muted">Email</span>
            <span class="text-bd-text-primary">{{ auth.user?.email }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-bd-text-muted">Role</span>
            <span class="text-bd-text-primary uppercase">{{ auth.user?.role }}</span>
          </div>
        </div>
      </div>
    </BdCard>

    <BdCard>
      <div class="p-6">
        <h2 class="mb-4 font-bd-sans text-lg font-semibold text-bd-text-primary">Change Password</h2>
        <form class="max-w-md space-y-4" @submit.prevent="changePassword">
          <BdInput v-model="passwordForm.current" type="password" label="Current Password" />
          <BdInput v-model="passwordForm.new" type="password" label="New Password" />
          <BdInput v-model="passwordForm.confirm" type="password" label="Confirm Password" />
          <p v-if="message" class="text-sm text-bd-warning">{{ message }}</p>
          <BdButton type="submit" variant="primary">Update Password</BdButton>
        </form>
      </div>
    </BdCard>
  </div>
</template>

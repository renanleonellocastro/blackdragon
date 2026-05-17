<script setup lang="ts">
import { onMounted, ref } from 'vue'
import BdCard from '@/components/ui/BdCard.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import api from '@/services/api'

interface BlogPost {
  id: string
  title: string
  slug: string
  excerpt: string | null
  published_at: string | null
  created_at: string
}

const posts = ref<BlogPost[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get<BlogPost[]>('/blog')
    posts.value = data
  } catch {
    // Blog may not have posts yet
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr: string | null): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
  <div class="min-h-screen bg-bd-bg-primary">
    <AppHeader />

    <section class="py-20">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <h1 class="bg-bd-metallic bg-clip-text font-bd-sans text-4xl font-bold text-transparent">
          Blog
        </h1>
        <p class="mt-4 text-lg text-bd-text-secondary">
          Technical articles, product updates, and automation insights.
        </p>

        <div v-if="loading" class="mt-12 text-center text-bd-text-muted">Loading...</div>

        <div v-else-if="posts.length === 0" class="mt-12 text-center text-bd-text-muted">
          No articles published yet. Check back soon!
        </div>

        <div v-else class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <BdCard v-for="post in posts" :key="post.id" hoverable>
            <router-link :to="`/blog/${post.slug}`" class="block p-6">
              <h3 class="font-bd-sans text-lg font-semibold text-bd-text-primary">
                {{ post.title }}
              </h3>
              <p v-if="post.excerpt" class="mt-2 text-sm text-bd-text-secondary line-clamp-3">
                {{ post.excerpt }}
              </p>
              <p class="mt-4 text-xs text-bd-text-muted">
                {{ formatDate(post.published_at) }}
              </p>
            </router-link>
          </BdCard>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

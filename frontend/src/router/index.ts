import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Public routes
    {
      path: '/',
      children: [
        { path: '', name: 'home', component: () => import('@/views/public/HomePage.vue') },
        { path: 'about', name: 'about', component: () => import('@/views/public/AboutPage.vue') },
        { path: 'products', name: 'products', component: () => import('@/views/public/ProductsPage.vue') },
        { path: 'solutions', name: 'solutions', component: () => import('@/views/public/SolutionsPage.vue') },
        { path: 'projects', name: 'projects', component: () => import('@/views/public/ProjectsPage.vue') },
        { path: 'blog', name: 'blog', component: () => import('@/views/public/BlogPage.vue') },
        { path: 'contact', name: 'contact', component: () => import('@/views/public/ContactPage.vue') },
      ],
    },
    // Auth routes
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginPage.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterPage.vue'),
    },
    // Portal routes (authenticated)
    {
      path: '/portal',
      component: () => import('@/components/layout/PortalLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'dashboard', component: () => import('@/views/portal/DashboardPage.vue') },
        { path: 'projects', name: 'project-list', component: () => import('@/views/portal/ProjectListPage.vue') },
        { path: 'projects/:id/editor', name: 'project-editor', component: () => import('@/views/portal/ProjectEditorPage.vue') },
        { path: 'boards', name: 'board-catalog', component: () => import('@/views/portal/BoardCatalogPage.vue') },
        { path: 'yaml/:id', name: 'yaml-preview', component: () => import('@/views/portal/YamlPreviewPage.vue') },
        { path: 'deployments', name: 'deployments', component: () => import('@/views/portal/DeploymentPage.vue') },
        { path: 'profile', name: 'profile', component: () => import('@/views/portal/ProfilePage.vue') },
        // Admin routes
        { path: 'admin/users', name: 'admin-users', component: () => import('@/views/portal/admin/UsersPage.vue'), meta: { requiresAdmin: true } },
        { path: 'admin/clients', name: 'admin-clients', component: () => import('@/views/portal/admin/ClientsPage.vue'), meta: { requiresAdmin: true } },
        { path: 'admin/boards', name: 'admin-boards', component: () => import('@/views/portal/admin/BoardManagementPage.vue'), meta: { requiresAdmin: true } },
        { path: 'admin/blog', name: 'admin-blog', component: () => import('@/views/portal/admin/BlogManagementPage.vue'), meta: { requiresAdmin: true } },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()

  if (to.matched.some((r) => r.meta.requiresAuth) && !auth.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  if (to.matched.some((r) => r.meta.requiresAdmin) && !auth.isAdmin) {
    return next({ name: 'dashboard' })
  }

  next()
})

export default router

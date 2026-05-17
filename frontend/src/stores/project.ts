import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ProjectItem } from '@/services/project.service'
import * as projectService from '@/services/project.service'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<ProjectItem[]>([])
  const currentProject = ref<ProjectItem | null>(null)
  const loading = ref(false)

  async function fetchProjects(propertyId?: string, status?: string) {
    loading.value = true
    try {
      projects.value = await projectService.listProjects(propertyId, status)
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id: string) {
    loading.value = true
    try {
      currentProject.value = await projectService.getProject(id)
    } finally {
      loading.value = false
    }
  }

  async function createProject(payload: projectService.ProjectCreate) {
    const project = await projectService.createProject(payload)
    projects.value.unshift(project)
    return project
  }

  async function deleteProject(id: string) {
    await projectService.deleteProject(id)
    projects.value = projects.value.filter((p) => p.id !== id)
    if (currentProject.value?.id === id) currentProject.value = null
  }

  async function duplicateProject(id: string) {
    const project = await projectService.duplicateProject(id)
    projects.value.unshift(project)
    return project
  }

  return { projects, currentProject, loading, fetchProjects, fetchProject, createProject, deleteProject, duplicateProject }
})

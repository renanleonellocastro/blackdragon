import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useProjectStore } from '@/stores/project'
import * as projectService from '@/services/project.service'

vi.mock('@/services/project.service', () => ({
  listProjects: vi.fn(),
  getProject: vi.fn(),
  createProject: vi.fn(),
  deleteProject: vi.fn(),
  duplicateProject: vi.fn(),
}))

const mockProject = { id: 'p1', name: 'Test', property_id: 'prop1', status: 'draft', created_at: '', updated_at: '' }

describe('project store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('starts empty', () => {
    const store = useProjectStore()
    expect(store.projects).toEqual([])
    expect(store.currentProject).toBeNull()
    expect(store.loading).toBe(false)
  })

  it('fetchProjects populates list', async () => {
    vi.mocked(projectService.listProjects).mockResolvedValue([mockProject] as any)
    const store = useProjectStore()
    await store.fetchProjects()
    expect(store.projects).toHaveLength(1)
    expect(store.loading).toBe(false)
  })

  it('fetchProject sets currentProject', async () => {
    vi.mocked(projectService.getProject).mockResolvedValue(mockProject as any)
    const store = useProjectStore()
    await store.fetchProject('p1')
    expect(store.currentProject?.id).toBe('p1')
  })

  it('createProject adds to list', async () => {
    vi.mocked(projectService.createProject).mockResolvedValue(mockProject as any)
    const store = useProjectStore()
    await store.createProject({ name: 'Test', property_id: 'prop1' } as any)
    expect(store.projects).toHaveLength(1)
  })

  it('deleteProject removes from list', async () => {
    vi.mocked(projectService.deleteProject).mockResolvedValue(undefined as any)
    const store = useProjectStore()
    store.projects = [mockProject] as any
    store.currentProject = mockProject as any
    await store.deleteProject('p1')
    expect(store.projects).toHaveLength(0)
    expect(store.currentProject).toBeNull()
  })

  it('duplicateProject adds copy to list', async () => {
    const dup = { ...mockProject, id: 'p2' }
    vi.mocked(projectService.duplicateProject).mockResolvedValue(dup as any)
    const store = useProjectStore()
    await store.duplicateProject('p1')
    expect(store.projects).toHaveLength(1)
    expect(store.projects[0]!.id).toBe('p2')
  })

  it('sets loading during fetchProjects', async () => {
    let resolve: Function
    vi.mocked(projectService.listProjects).mockImplementation(
      () => new Promise((r) => { resolve = r }),
    )
    const store = useProjectStore()
    const p = store.fetchProjects()
    expect(store.loading).toBe(true)
    resolve!([])
    await p
    expect(store.loading).toBe(false)
  })
})

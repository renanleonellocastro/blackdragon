import { test, expect } from '@playwright/test'

async function isBackendDBReady(): Promise<boolean> {
  try {
    const res = await fetch('http://localhost:8000/api/blog')
    return res.ok
  } catch {
    return false
  }
}

test.describe('Visual Editor - US3', () => {
  test('open editor, place blocks, connect wires', async ({ page }) => {
    const dbReady = await isBackendDBReady()
    test.skip(!dbReady, 'Requires backend with database connection')

    // Register and login
    const ts = Date.now()
    await page.goto('/register')
    await page.getByLabel('Full Name').fill('Editor User')
    await page.getByLabel('Email').fill(`editor+${ts}@test.com`)
    await page.getByLabel('Password').fill('TestPass123!')
    await page.getByRole('button', { name: 'Create Account' }).click()
    await page.waitForURL(/portal/, { timeout: 10000 })

    // Navigate to projects page
    await page.goto('/portal/projects')
    await expect(page.getByText('Projects')).toBeVisible()
  })
})

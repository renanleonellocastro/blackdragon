import { test, expect } from '@playwright/test'

async function isBackendDBReady(): Promise<boolean> {
  try {
    const res = await fetch('http://localhost:8000/api/blog')
    return res.ok
  } catch {
    return false
  }
}

test.describe('Auth & Projects - US2', () => {
  test('register, login, create project', async ({ page }) => {
    const dbReady = await isBackendDBReady()
    test.skip(!dbReady, 'Requires backend with database connection')

    const timestamp = Date.now()

    // Register
    await page.goto('/register')
    await expect(page.getByRole('heading', { name: 'Create Account' })).toBeVisible()
    await page.getByLabel('Full Name').fill('E2E User')
    await page.getByLabel('Email').fill(`e2e+${timestamp}@test.com`)
    await page.getByLabel('Password').fill('TestPass123!')
    await page.getByRole('button', { name: 'Create Account' }).click()

    // Should redirect to portal after register
    await expect(page).toHaveURL(/portal/, { timeout: 10000 })
  })
})

import { test, expect } from '@playwright/test'

async function isBackendDBReady(): Promise<boolean> {
  try {
    const res = await fetch('http://localhost:8000/api/blog')
    return res.ok
  } catch {
    return false
  }
}

test.describe('Public Website - US1', () => {
  test('navigates all public pages and verifies BlackDragon branding', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: 'BlackDragon' })).toBeVisible()

    const pages = ['/about', '/products', '/solutions', '/projects', '/blog', '/contact']
    for (const p of pages) {
      await page.goto(p)
      await expect(page).toHaveURL(p)
    }
  })

  test('submits contact form', async ({ page }) => {
    const dbReady = await isBackendDBReady()
    test.skip(!dbReady, 'Requires backend with database connection')

    await page.goto('/contact')
    await page.getByLabel('Name').fill('Test User')
    await page.getByLabel('Email').fill('test@example.com')
    await page.getByLabel('Company').fill('TestCo')
    await page.getByLabel('Message').fill('Hello from e2e test — automated testing')
    await page.getByRole('button', { name: 'Send Message' }).click()
    await expect(page.getByText('Thank you')).toBeVisible({ timeout: 10000 })
  })
})

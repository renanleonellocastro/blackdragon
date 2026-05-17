import { test, expect } from '@playwright/test'

test.describe('Public Website - US1', () => {
  test('navigates all public pages and verifies BlackDragon branding', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('text=BlackDragon')).toBeVisible()

    const pages = ['/about', '/products', '/solutions', '/projects', '/blog', '/contact']
    for (const p of pages) {
      await page.goto(p)
      await expect(page).toHaveURL(p)
    }
  })

  test('submits contact form', async ({ page }) => {
    await page.goto('/contact')
    await page.fill('[name="name"]', 'Test User')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="company"]', 'TestCo')
    await page.fill('[name="message"]', 'Hello from e2e test')
    await page.click('button[type="submit"]')
    // Should show success or navigate
    await expect(page.locator('text=Thank')).toBeVisible({ timeout: 5000 })
  })
})

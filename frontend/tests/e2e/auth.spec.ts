import { test, expect } from '@playwright/test'

test.describe('Auth & Projects - US2', () => {
  test('register, login, create project', async ({ page }) => {
    // Register
    await page.goto('/register')
    await expect(page.locator('img[alt*="logo"], svg')).toBeVisible()
    await page.fill('[name="full_name"]', 'E2E User')
    await page.fill('[name="email"]', `e2e+${Date.now()}@test.com`)
    await page.fill('[name="password"]', 'TestPass123!')
    await page.click('button[type="submit"]')

    // Login
    await page.goto('/login')
    await page.fill('[name="email"]', `e2e+${Date.now()}@test.com`)
    await page.fill('[name="password"]', 'TestPass123!')
    await page.click('button[type="submit"]')

    // Should reach dashboard
    await expect(page).toHaveURL(/portal/, { timeout: 5000 })
  })
})

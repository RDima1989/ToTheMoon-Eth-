import { test, expect } from "@playwright/test";

test.describe("Registration form", () => {
  test("submits successfully with valid data", async ({ page }) => {
    await page.goto("/register");

    await page.getByLabel("Email").fill("test.user@example.com");
    await page.getByLabel("Password").fill("StrongPass123!");
    await page.getByLabel("Confirm Password").fill("StrongPass123!");

    await page.getByRole("button", { name: /register/i }).click();

    await expect(
      page.getByRole("heading", { name: /welcome|success/i }),
    ).toBeVisible();
  });

  test("shows validation errors for empty fields", async ({ page }) => {
    await page.goto("/register");

    await page.getByRole("button", { name: /register/i }).click();

    await expect(page.getByText(/email.*required/i)).toBeVisible();
    await expect(page.getByText(/password.*required/i)).toBeVisible();
  });
});

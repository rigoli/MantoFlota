import { expect, test } from "@playwright/test";

test("home muestra MantoFlota", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "MantoFlota" })).toBeVisible();
});

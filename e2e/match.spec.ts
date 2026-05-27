import { expect, test } from "@playwright/test";

test("submitting a role shows ranked candidates with explanations", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByLabel("Role title").fill("Backend Engineer");
  await page.getByLabel("Required skills").fill("python, postgres, docker");
  await page.getByLabel("Minimum years").fill("5");
  await page.getByRole("button", { name: "Match candidates" }).click();

  const cards = page.getByTestId("match-card");
  await expect(cards.first()).toBeVisible();
  await expect(cards.first()).toContainText("Satisfies");
  expect(await cards.count()).toBeGreaterThan(0);
});

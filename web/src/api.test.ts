import { parseSkills } from "./api";

test("parseSkills trims, splits, and drops empties", () => {
  expect(parseSkills("python, react ,, typescript ")).toEqual([
    "python",
    "react",
    "typescript",
  ]);
});

test("parseSkills returns empty array for blank input", () => {
  expect(parseSkills("   ")).toEqual([]);
});

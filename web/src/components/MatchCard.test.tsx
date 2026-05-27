import { render, screen } from "@testing-library/react";
import { MatchCard } from "./MatchCard";
import type { Match } from "../types";

const match: Match = {
  id: "c001",
  name: "Ada Reyes",
  title: "Senior Backend Engineer",
  score: 0.82,
  breakdown: {
    skill_coverage: 1.0,
    experience_fit: 1.0,
    semantic_similarity: 0.4,
  },
  satisfied: [{ requirement: "python", matched_skill: "python" }],
  missing_requirements: ["rust"],
  explanation: "Satisfies 1 requirement(s): python via python. Missing: rust.",
};

test("shows the candidate, score, and grounded skill chips", () => {
  render(<MatchCard match={match} rank={1} />);
  expect(screen.getByText("Ada Reyes")).toBeInTheDocument();
  expect(screen.getByText("82")).toBeInTheDocument();
  expect(screen.getByText("python")).toBeInTheDocument();
  expect(screen.getByText("rust")).toBeInTheDocument();
});

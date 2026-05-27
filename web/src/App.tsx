import { useState } from "react";
import { parseSkills, requestMatch } from "./api";
import { MatchCard } from "./components/MatchCard";
import type { MatchReport } from "./types";

export default function App() {
  const [title, setTitle] = useState("Backend Engineer");
  const [skills, setSkills] = useState("python, postgres, docker");
  const [minYears, setMinYears] = useState(5);
  const [report, setReport] = useState<MatchReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await requestMatch({
        title,
        required_skills: parseSkills(skills),
        min_years: minYears,
        top_k: 5,
      });
      setReport(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="app__header">
        <h1>TalentAgent</h1>
        <p>Match candidate profiles to a role with grounded, ranked explanations.</p>
      </header>

      <form className="role-form" onSubmit={onSubmit}>
        <label>
          Role title
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            aria-label="Role title"
          />
        </label>
        <label>
          Required skills (comma separated)
          <input
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            aria-label="Required skills"
          />
        </label>
        <label>
          Minimum years
          <input
            type="number"
            min={0}
            value={minYears}
            onChange={(e) => setMinYears(Number(e.target.value))}
            aria-label="Minimum years"
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Matching..." : "Match candidates"}
        </button>
      </form>

      {error && <p className="banner banner--error">{error}</p>}

      {report && (
        <section className="results">
          {report.needs_review ? (
            <p className="banner banner--review" data-testid="review-banner">
              Flagged for human review: {report.review_reason} (confidence{" "}
              {Math.round(report.confidence * 100)}%)
            </p>
          ) : (
            <p className="banner banner--ok" data-testid="confident-banner">
              Confident match: {report.review_reason} (confidence{" "}
              {Math.round(report.confidence * 100)}%)
            </p>
          )}
          {report.matches.map((m, i) => (
            <MatchCard key={m.id} match={m} rank={i + 1} />
          ))}
        </section>
      )}
    </main>
  );
}

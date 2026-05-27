import type { Match } from "../types";
import { ScoreBar } from "./ScoreBar";

interface Props {
  match: Match;
  rank: number;
}

export function MatchCard({ match, rank }: Props) {
  return (
    <article className="match-card" data-testid="match-card">
      <header className="match-card__head">
        <span className="match-card__rank">#{rank}</span>
        <div>
          <h3 className="match-card__name">{match.name}</h3>
          <p className="match-card__title">{match.title}</p>
        </div>
        <span className="match-card__score">{Math.round(match.score * 100)}</span>
      </header>

      <p className="match-card__explanation">{match.explanation}</p>

      <div className="match-card__skills">
        {match.satisfied.map((e) => (
          <span key={e.requirement} className="chip chip--hit">
            {e.requirement}
          </span>
        ))}
        {match.missing_requirements.map((req) => (
          <span key={req} className="chip chip--miss">
            {req}
          </span>
        ))}
      </div>

      <div className="match-card__bars">
        <ScoreBar label="Skill coverage" value={match.breakdown.skill_coverage} />
        <ScoreBar label="Experience fit" value={match.breakdown.experience_fit} />
        <ScoreBar
          label="Semantic similarity"
          value={match.breakdown.semantic_similarity}
        />
      </div>
    </article>
  );
}

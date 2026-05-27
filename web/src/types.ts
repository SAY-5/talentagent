export interface Evidence {
  requirement: string;
  matched_skill: string;
}

export interface ScoreBreakdown {
  skill_coverage: number;
  experience_fit: number;
  semantic_similarity: number;
}

export interface Match {
  id: string;
  name: string;
  title: string;
  score: number;
  breakdown: ScoreBreakdown;
  satisfied: Evidence[];
  missing_requirements: string[];
  explanation: string;
}

export interface MatchReport {
  role: { title: string; required_skills: string[]; min_years: number };
  needs_review: boolean;
  review_reason: string;
  confidence: number;
  matches: Match[];
}

export interface RoleRequest {
  title: string;
  required_skills: string[];
  min_years: number;
  top_k: number;
}

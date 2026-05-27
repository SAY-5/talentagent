import type { MatchReport, RoleRequest } from "./types";

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function requestMatch(req: RoleRequest): Promise<MatchReport> {
  const resp = await fetch(`${BASE}/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!resp.ok) {
    throw new Error(`match request failed: ${resp.status}`);
  }
  return resp.json() as Promise<MatchReport>;
}

export function parseSkills(raw: string): string[] {
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

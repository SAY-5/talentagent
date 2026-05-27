# TalentAgent

TalentAgent is a goal-oriented agent that matches candidate profiles to a role.
Given a role and its requirements, it gathers candidates by calling a search
backend, retrieves and ranks them through an embedding pipeline, and returns a
ranked list where every result carries a grounded explanation. When the top
result is weak or the field is ambiguous, the agent flags the result set for
human review instead of asserting a confident match.

## What it does

- **Goal-oriented loop.** From a role, the agent tool-calls the search backend
  (`search_candidates`, `filter_by_skill`, `get_profile`) to assemble a
  candidate pool, then ranks it.
- **Retrieval over embeddings.** Roles and profiles are embedded behind a
  provider seam; semantic similarity is one component of the score. The default
  provider is a deterministic local embedding so runs are reproducible offline.
- **Explainable ranking.** Each match reports a score breakdown (skill
  coverage, experience fit, semantic similarity), the requirements it satisfies
  with the matched skill as evidence, and the requirements it misses.
- **Grounded explanations.** Evidence is built only from skills the candidate
  actually lists, so an explanation can never cite a requirement the candidate
  does not meet.
- **Confidence-gated review.** A review gate inspects the top score and the
  margin to the runner-up. A clear top match returns confidently; a low-signal
  or ambiguous result set is flagged for review.
- **Web interface.** A React and TypeScript app to enter a role and read the
  ranked candidates, their explanations, score breakdowns, and the review flag.

## Layout

```
src/talentagent/   agent core, tools, search backend, ranking, confidence, API
tests/             Python tests (unit, contract, ranking quality, review gate)
web/               React + TypeScript interface
e2e/               Playwright test against the compose stack
bench/             match-path benchmark
```

## Running

Backend:

```
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
uvicorn talentagent.api:app --reload
```

Frontend:

```
cd web && npm install && npm run dev
```

Or the whole stack:

```
docker compose up --build
```

The API serves on `:8000`, the web app on `:5173`.

## The provider seam

The agent depends on an `EmbeddingProvider` protocol, not a concrete model. The
default `HashingEmbeddingProvider` maps text to a vector with feature hashing,
which is deterministic and needs no network. A hosted embedding provider can be
substituted by implementing the same protocol, without changing the agent or
ranking code.

## How this differs

This project sits alongside a few neighbours with a distinct angle:

- **agentdesk** is a customer-operations agent with a human handoff; its goal is
  resolving support threads, not matching.
- **vectorsearch** is raw vector search over a corpus; it returns nearest
  neighbours without ranking explanations or a review decision.
- **talentllm** and **insightllm** are question-answering assistants over a
  knowledge base.

TalentAgent is the candidate-to-role matching agent: goal-oriented matching
plus grounded, explainable ranking plus a confidence-gated review step. The
explanation and the review decision are the point, not just a similarity score.

## License

MIT. See [LICENSE](LICENSE).

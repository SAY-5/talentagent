"""Smoke gate for match-path throughput regression.

Runs the benchmark, compares candidates-per-second against the committed
baseline, and exits non-zero if throughput drops by more than the allowed
fraction. The default budget is 30 percent, which absorbs CI runner variance
while still catching a real slowdown.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from match_bench import run

ALLOWED_REGRESSION = 0.30


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default=str(Path(__file__).with_name("baseline.json")))
    parser.add_argument("--size", type=int, default=5000)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()

    baseline = json.loads(Path(args.baseline).read_text())
    current = run(args.size, args.repeats)
    print(json.dumps(current))

    base_tput = baseline["candidates_per_second"]
    cur_tput = current["candidates_per_second"]
    floor = base_tput * (1.0 - ALLOWED_REGRESSION)
    if cur_tput < floor:
        print(
            f"regression: {cur_tput:.1f}/s below floor {floor:.1f}/s "
            f"(baseline {base_tput:.1f}/s)",
            file=sys.stderr,
        )
        return 1
    print(f"ok: {cur_tput:.1f}/s within 30% of baseline {base_tput:.1f}/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Template: run a planning-phases plan with one fresh Cursor agent session per
phase.

Copy this file into the project (for example `scripts/run_phases.py`), fill in
the CONFIG block, then:

  python3 scripts/run_phases.py
  python3 scripts/run_phases.py --start-phase 2 --end-phase 3
  python3 scripts/run_phases.py --help

Requirements:
  - `agent` on PATH (Cursor headless CLI)
  - Headless auth already working (`agent login` or `CURSOR_API_KEY`)

Behavior:
  - New `agent` process per phase
  - Self-contained prompt; plan file is the source of truth for scope
  - Exit gates after each phase; fail-fast
  - Logs under LOG_DIR
  - Never commits
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — fill in when copying this template into a project
# ---------------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
# Directory that contains this script's project root (edit if nested deeper).
PROJECT_ROOT = SCRIPT_PATH.parent.parent
# Workspace passed to `agent --workspace` (often a monorepo parent).
WORKSPACE_ROOT = PROJECT_ROOT
PLAN_PATH = PROJECT_ROOT / "docs/planning/REPLACE-WITH-PLAN.md"
LOG_DIR = PROJECT_ROOT / "tmp/phase-runner-logs"
SENTINEL_PREFIX = "PHASE_RUNNER"


@dataclass(frozen=True)
class Phase:
    number: int
    name: str
    # Each gate is (argv, cwd). Empty list means "DONE tag + sentinel only".
    exit_gates: list[tuple[list[str], Path]] = field(default_factory=list)


# Implementation phases only (phase 0 wrote this script and is already DONE).
PHASES: dict[int, Phase] = {
    1: Phase(
        number=1,
        name="replace with phase 1 name",
        exit_gates=[
            (["make", "test"], PROJECT_ROOT),
        ],
    ),
    # 2: Phase(
    #     number=2,
    #     name="replace with phase 2 name",
    #     exit_gates=[
    #         (["npm", "test"], PROJECT_ROOT / "other-package"),
    #     ],
    # ),
}

# ---------------------------------------------------------------------------
# Runner — usually leave as-is
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run plan phases with one fresh Cursor agent session each.",
    )
    parser.add_argument(
        "--start-phase",
        type=int,
        default=min(PHASES),
        choices=sorted(PHASES),
        help="First phase to run.",
    )
    parser.add_argument(
        "--end-phase",
        type=int,
        default=max(PHASES),
        choices=sorted(PHASES),
        help="Last phase to run.",
    )
    parser.add_argument(
        "--agent-bin",
        default="agent",
        help="Agent CLI binary (default: agent).",
    )
    return parser.parse_args()


def run_checked(
    command: list[str],
    *,
    cwd: Path,
    log_path: Path | None = None,
    description: str,
) -> subprocess.CompletedProcess[str]:
    print(f"[phase-runner] {description}")
    print(f"[phase-runner] cwd={cwd}")
    print(f"[phase-runner] cmd={' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            "\n".join(
                [
                    f"# description: {description}",
                    f"# cwd: {cwd}",
                    f"# exit_code: {result.returncode}",
                    "",
                    "## stdout",
                    result.stdout,
                    "",
                    "## stderr",
                    result.stderr,
                    "",
                ]
            ),
            encoding="utf-8",
        )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(
            result.stderr,
            file=sys.stderr,
            end="" if result.stderr.endswith("\n") else "\n",
        )
    return result


def ensure_agent_available(agent_bin: str) -> None:
    if shutil.which(agent_bin) is None:
        raise SystemExit(f"`{agent_bin}` is not on PATH.")


def ensure_plan_exists() -> None:
    if not PLAN_PATH.exists():
        raise SystemExit(f"Plan file not found: {PLAN_PATH}")
    if "REPLACE-WITH-PLAN" in str(PLAN_PATH):
        raise SystemExit("Fill in PLAN_PATH in the CONFIG block before running.")


def preflight_auth(agent_bin: str) -> None:
    probe_log = LOG_DIR / "preflight-auth.log"
    result = run_checked(
        [
            agent_bin,
            "--print",
            "--trust",
            "--workspace",
            str(WORKSPACE_ROOT),
            "Reply exactly with AUTH_OK.",
        ],
        cwd=WORKSPACE_ROOT,
        log_path=probe_log,
        description="Preflight Cursor agent authentication",
    )
    if result.returncode != 0 or "AUTH_OK" not in result.stdout:
        raise SystemExit(
            "Headless Cursor agent authentication failed. "
            f"See {probe_log}; run `agent login` or set CURSOR_API_KEY, then rerun."
        )


def build_phase_prompt(phase: Phase) -> str:
    return f"""You are running phase {phase.number} ({phase.name}).

Plan file: `{PLAN_PATH}`
Workspace: `{WORKSPACE_ROOT}`

Read the plan first. Treat it as the single source of truth.

Implement only phase {phase.number} as specified in the plan.

Rules:
- Stay inside that phase's scope.
- On success, update that phase's heading in the plan to include `— DONE`.
- Do not start other phases.
- Do not create a git commit or push.

Final response requirements:
- Start with `{SENTINEL_PREFIX}: PHASE_{phase.number}_COMPLETE`
- Briefly say what changed and what you verified.
"""


def run_phase(agent_bin: str, phase: Phase) -> Path:
    log_path = LOG_DIR / f"phase-{phase.number}.log"
    result = run_checked(
        [
            agent_bin,
            "--print",
            "--trust",
            "--force",
            "--workspace",
            str(WORKSPACE_ROOT),
            build_phase_prompt(phase),
        ],
        cwd=WORKSPACE_ROOT,
        log_path=log_path,
        description=f"Run phase {phase.number}: {phase.name}",
    )
    if result.returncode != 0:
        raise SystemExit(f"Phase {phase.number} agent run failed. See {log_path}.")
    sentinel = f"{SENTINEL_PREFIX}: PHASE_{phase.number}_COMPLETE"
    if sentinel not in result.stdout:
        raise SystemExit(
            f"Phase {phase.number} output missing sentinel `{sentinel}`. "
            f"See {log_path}."
        )
    return log_path


def _phase_heading_line(plan_text: str, phase_number: int) -> str:
    prefix = f"### {phase_number}."
    for line in plan_text.splitlines():
        if line.startswith(prefix):
            return line
    # Also accept "## N." style headings.
    prefix = f"## {phase_number}."
    for line in plan_text.splitlines():
        if line.startswith(prefix):
            return line
    return ""


def assert_plan_heading_done(phase_number: int) -> None:
    plan_text = PLAN_PATH.read_text(encoding="utf-8")
    heading = _phase_heading_line(plan_text, phase_number)
    if not heading:
        raise SystemExit(
            f"Phase {phase_number} heading not found in {PLAN_PATH}."
        )
    if "— DONE" not in heading and "- DONE" not in heading:
        raise SystemExit(
            f"Phase {phase_number} is not marked DONE in {PLAN_PATH}."
        )


def run_exit_gates(phase: Phase) -> None:
    assert_plan_heading_done(phase.number)
    for index, (argv, cwd) in enumerate(phase.exit_gates, start=1):
        log_path = LOG_DIR / f"phase-{phase.number}-gate-{index}.log"
        result = run_checked(
            argv,
            cwd=cwd,
            log_path=log_path,
            description=f"Phase {phase.number} exit gate {index}: {' '.join(argv)}",
        )
        if result.returncode != 0:
            raise SystemExit(
                f"Phase {phase.number} exit gate {index} failed. See {log_path}."
            )


def main() -> int:
    args = parse_args()
    if args.start_phase > args.end_phase:
        raise SystemExit("--start-phase must be <= --end-phase.")
    if not PHASES:
        raise SystemExit("PHASES is empty; fill in the CONFIG block.")
    ensure_agent_available(args.agent_bin)
    ensure_plan_exists()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    preflight_auth(args.agent_bin)
    for phase_number in range(args.start_phase, args.end_phase + 1):
        phase = PHASES[phase_number]
        print(f"[phase-runner] starting phase {phase.number}: {phase.name}")
        run_phase(args.agent_bin, phase)
        run_exit_gates(phase)
        print(f"[phase-runner] phase {phase.number} passed")
    print("[phase-runner] all requested phases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

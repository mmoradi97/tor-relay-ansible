#!/usr/bin/env python3
"""Snowflake stats helper (role-local copy).

This is identical in purpose to scripts/snowflake_stats.py but is installed onto
the target host by the app_snowflake role.

No operator identifiers or host metadata are embedded.
"""

import argparse
import re
import subprocess
import sys

p_conn = re.compile(r"there were\s+(\d+)\s+completed successful connections", re.I)
p_down = re.compile(r"↓\s+(\d+)\s+KB")
p_up = re.compile(r"↑\s+(\d+)\s+KB")


def grab_logs(container: str, since: str) -> str:
    try:
        return subprocess.check_output(
            ["docker", "logs", "--since", since, container],
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        return e.output


def pick_container(preferred: str | None = None) -> str | None:
    names = subprocess.check_output(
        ["docker", "ps", "--format", "{{.Names}}"],
        text=True,
    ).splitlines()

    if preferred and preferred in names:
        return preferred

    for cand in ("snowflake-proxy", "snowflake"):
        if cand in names:
            return cand

    return preferred or (names[0] if names else None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="24h", help='Docker "--since" window (default: 24h)')
    ap.add_argument("--container", help="Container name (defaults to auto-detect)")
    args = ap.parse_args()

    container = pick_container(args.container)
    if not container:
        print("ERROR: No running docker containers found matching snowflake.", file=sys.stderr)
        return 1

    logs = grab_logs(container, args.since)
    if not logs.strip():
        print(f"No logs found for {container} in the last {args.since}.")
        return 0

    conn = 0
    down = 0
    up = 0

    for line in logs.splitlines():
        m = p_conn.search(line)
        if m:
            conn += int(m.group(1))

        md = p_down.search(line)
        if md:
            down += int(md.group(1))

        mu = p_up.search(line)
        if mu:
            up += int(mu.group(1))

    def gb(kb: int) -> float:
        return kb / 1024 / 1024

    ratio = (down / up) if up else 0.0

    print(f"Container  : {container}")
    print(f"Window     : {args.since}")
    print(f"Connections: {conn}")
    print(f"Down       : {gb(down):.2f} GB")
    print(f"Up         : {gb(up):.2f} GB")
    print(f"Ratio      : {ratio:.1f}:1" if up else "Ratio      : ∞ (no upload counted)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

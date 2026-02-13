#!/usr/bin/env python3
"""Relay status checker (public-safe template).

This script queries Onionoo (a public Tor relay data source) for one or more relay
fingerprints and prints a short status report.

This public repository ships with **no** real fingerprints. Provide your own via
CLI flags.

Example:
  python3 scripts/check_relays.py --fingerprint ABCDEF... --fingerprint 012345...
"""

import argparse
import sys
from typing import List

import requests

# ANSI colors
ORANGE = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"


def check_relays(fingerprints: List[str], show_address: bool = True) -> int:
    lookup_str = ",".join(fingerprints)
    url = f"https://onionoo.torproject.org/details?lookup={lookup_str}"

    print(f"Fetching data for {len(fingerprints)} relays...")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return 2

    relays_found = {r.get("fingerprint"): r for r in data.get("relays", [])}

    print("\n" + "=" * 70)

    for fp in fingerprints:
        relay = relays_found.get(fp)

        print(f"RELAY: {BOLD}{fp}{RESET}")

        if not relay:
            print("  [!] STATUS: NOT FOUND")
            print("-" * 70)
            continue

        nickname = relay.get("nickname", "Unknown")
        last_seen = relay.get("last_seen", "Never")
        running = bool(relay.get("running", False))

        country_code = str(relay.get("country", "??")).upper()
        country_name = relay.get("country_name", "Unknown")

        status_str = f"{GREEN}RUNNING{RESET}" if running else f"{RED}OFFLINE{RESET}"

        print(f"  Nickname:    {nickname}")
        print(f"  Location:    {CYAN}{country_name} ({country_code}){RESET}")
        print(f"  Status:      {status_str}")
        print(f"  Last seen:   {ORANGE}{last_seen} (UTC){RESET}")

        # Optional: address/rDNS can be sensitive in some contexts.
        if show_address:
            hostnames = relay.get("verified_host_names", []) or relay.get("unverified_host_names", [])
            if hostnames:
                address_display = hostnames[0]
            else:
                or_addresses = relay.get("or_addresses", ["Unknown"])
                address_display = str(or_addresses[0]).split(":")[0]
            print(f"  Address/DNS: {CYAN}{address_display}{RESET}")

        adv_bw_mb = float(relay.get("advertised_bandwidth", 0)) / 1024 / 1024
        weight = int(relay.get("consensus_weight", 0))
        print(f"  Bandwidth:   {adv_bw_mb:.2f} MB/s")
        print(f"  Weight:      {weight}")

        print("-" * 70)

    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--fingerprint",
        action="append",
        default=[],
        help="Relay fingerprint (repeat flag for multiple relays)",
    )
    ap.add_argument(
        "--no-address",
        action="store_true",
        help="Do not display address/rDNS fields from Onionoo",
    )
    args = ap.parse_args()

    fps = [f.strip() for f in args.fingerprint if f and f.strip()]
    if not fps:
        ap.error("Provide at least one --fingerprint value.")

    return check_relays(fps, show_address=not args.no_address)


if __name__ == "__main__":
    raise SystemExit(main())

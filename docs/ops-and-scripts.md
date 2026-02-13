# Ops playbooks and scripts (public template)

This repository includes operational playbooks (`ops/`) and helper scripts (`scripts/`) intended for day-2 operations (updates, backups/restores, and basic visibility).

This public repo ships **no** real inventory, hosts, fingerprints, contact info, onion addresses, or provider identifiers.

## Ops playbooks (`ops/`)

Operational playbooks are generally safe to run repeatedly, but they may perform writes (e.g., upgrades, backups) and may require Ansible Vault access.

- `ops/update_fleet.yml`
  - Purpose: Apply OS/package updates across hosts.
  - Notes: Prefer running with `--limit` (group or single host) first.

- `ops/tor_identity_backup.yml`
  - Purpose: Back up Tor identity material from hosts and store vault-encrypted archives locally.
  - Notes: In this public template, encrypted outputs are written under `.local/tor_identity/` (gitignored by default).

- `ops/tor_identity_encrypt_one.yml`
  - Purpose: Helper for encrypting a single identity archive with Ansible Vault.

- `ops/snowflake_stats.yml`
  - Purpose: Aggregate Snowflake proxy stats from hosts.
  - Notes: The playbook targets the `snowflake` inventory group by default.

Other playbooks may be added/ported over time (e.g., traffic/geo summaries). If you port additional playbooks from elsewhere, ensure they do not embed environment-specific identifiers.

## Scripts (`scripts/`)

Scripts provide quick local checks and parsing of public/remote data sources.

- `scripts/check_relays.py`
  - Purpose: Query Onionoo for one or more relay fingerprints and print a status report.
  - Notes: This public repo does not include any real fingerprints; provide them via CLI flags.

- `scripts/snowflake_stats.py`
  - Purpose: Collect/format Snowflake statistics by parsing Docker logs.

## Related docs

- `docs/tor-identity.md`: background and details on identity handling workflows in this repo.

[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Ansible](https://img.shields.io/badge/ansible-playbooks-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)

# tor-relay-ansible

Public, sanitized Ansible repo for running Tor relays and related apps.

## Docs

- [App toggles (enable/disable + hard-remove)](docs/app-toggles.md)
- [Ops playbooks and scripts](docs/ops-and-scripts.md)
- [Tor identity details](docs/tor-identity.md)

## What this repo does

- Baseline roles:
  - `os_baseline`: OS-level baseline (packages, time sync, host settings, etc.).
  - `security_baseline`: security baseline (SSH hardening, firewall/UFW, fail2ban, etc.).

- App roles:
  - `app_tor`: install and configure Tor.
  - `app_snowflake`: Snowflake proxy.
  - `app_conduit`: Conduit.

## App toggles (enable/disable)

This repo supports per-group and per-host toggles that control whether an app is installed or **hard-removed** on the next run.

- `app_tor_enabled`
- `app_snowflake_enabled`
- `app_conduit_enabled`

Important:

- If `app_*_enabled: true`, the role installs/configures the app.
- If `app_*_enabled: false`, the role uninstalls the app and removes what it manages (containers/volumes/files/packages).

## Inventory layout

This repo uses directory-based vars:

- Defaults: `inventory/group_vars/all/`
- Per-group: `inventory/group_vars/<group>/`
- Per-host: `inventory/host_vars/<host>/`

Example toggle files:

- `inventory/group_vars/all/app_toggles.yml`
- `inventory/group_vars/tsc/app_toggles.yml`
- `inventory/group_vars/sc/app_toggles.yml`
- `inventory/host_vars/<host>/app_toggles.yml` (optional override)

## Common commands

Run Conduit on a group (skip baseline dependencies)

```bash
ansible-playbook -i inventory/hosts.ini playbooks/conduit.yml \
  --limit <group-or-host> --tags app_conduit --skip-tags deps
```

Hard-remove Conduit from TSC (Tor relays)

```bash
ansible-playbook -i inventory/hosts.ini playbooks/conduit.yml \
  --limit tsc --skip-tags deps
```

Run only baselines

```bash
ansible-playbook -i inventory/hosts.ini playbooks/os_baseline.yml
ansible-playbook -i inventory/hosts.ini playbooks/security_baseline.yml
```

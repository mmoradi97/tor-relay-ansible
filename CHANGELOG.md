# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-07

### Added
- GitHub Actions workflow for `ansible-lint` on push and PR
- `.ansible-lint` config to exclude collections, warn on style rules
- `CHANGELOG.md`
- README badges: lint CI, Ansible, license, release

## [1.0.0] - 2026-04-07

### Added
- Initial public release
- `os_baseline` role: packages, time sync, host settings
- `security_baseline` role: SSH hardening, UFW, fail2ban
- `app_tor` role: Tor relay install and configuration
- `app_snowflake` role: Snowflake proxy
- `app_conduit` role: Conduit
- Per-group and per-host app toggles (`app_*_enabled`)
- Playbooks: `tor.yml`, `snowflake.yml`, `conduit.yml`, `os_baseline.yml`, `security_baseline.yml`
- `inventory.example/` with `hosts.ini`, `group_vars/`, `host_vars/`
- `ansible.cfg`, `requirements.yml`
- Docs: app-toggles, ops-and-scripts, tor-identity
- `.gitignore` excluding private inventory, secrets, vault files

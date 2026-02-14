# tor-relay-ansible [![License](https://img.shields.io/github/license/mmoradi97/tor-relay-ansible)](./LICENSE) [![Ansible](https://img.shields.io/badge/ansible-playbooks-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/) [![community.general](https://img.shields.io/badge/community.general-10.7.0-blue)](./collections/requirements.yml)

An Ansible repo to manage hosts running Tor relays, Snowflake proxies, and a Conduit container, plus baseline hardening and ops utilities.

This repository is published in a **public-safe** form: it intentionally contains no real inventory, host metadata, or Tor identity artifacts.

## Repository layout
- `playbooks/` – entrypoints you run (baseline + apps).
- `roles/` – implementation roles (`os_baseline`, `security_baseline`, `app_tor`, `app_snowflake`, `app_conduit`, `monitoring_hetrixtools`).
- `ops/` – utility playbooks (fleet updates, stats, geo summaries, identity backup/restore helpers).
- `collections/requirements.yml` – pinned Ansible collections for reproducible installs.
- `inventory.example/` – example inventory structure (copy into your private inventory).

## Playbooks
- `playbooks/os_baseline.yml` – OS baseline (packages, time sync, docker optional).
- `playbooks/security_baseline.yml` – SSH hardening + UFW + fail2ban.
- `playbooks/tor.yml` – Tor relay role.
- `playbooks/snowflake.yml` – Snowflake proxy role.
- `playbooks/conduit.yml` – Conduit role.

## Quickstart
1) Install collections (pinned):

```bash
ansible-galaxy collection install -r collections/requirements.yml
(Optional) Install Galaxy roles if you use requirements.yml:

bash
ansible-galaxy role install -r requirements.yml
Create your private inventory:

Copy inventory.example/ to a new local inventory/

Put real hosts/vars in inventory/ and keep it out of git

Run a baseline then an app playbook:

bash
ansible-playbook -i inventory/ playbooks/os_baseline.yml
ansible-playbook -i inventory/ playbooks/security_baseline.yml
ansible-playbook -i inventory/ playbooks/tor.yml
Privacy / safety
No real inventories, IPs, fingerprints, contact strings, or identity archives should be committed here.

Tor identity material must stay private; the repo only keeps placeholder paths (e.g. roles/app_tor/files/identity/).

Notes on badges
The community.general badge is set to 10.7.0 to match collections/requirements.yml. Update it if you change the pin.

License
MIT (see LICENSE).

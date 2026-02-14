# roles/galaxy

This directory existed in the private repo to vendor Ansible Galaxy roles.

In this public repository, we do **not** vendor third-party Galaxy roles under `roles/galaxy/`.

## What to do instead
Use `requirements.yml` / `collections/requirements.yml` and install dependencies:

- `ansible-galaxy role install -r requirements.yml`
- `ansible-galaxy collection install -r collections/requirements.yml`

## Why
Vendoring third-party roles bloats the repo and complicates licensing/updates.

# Tor identity backup/restore (public template)

This repository includes optional operational playbooks to help you preserve a relay’s Tor identity (keys) across rebuilds.

## Two modes

- New identity: let Tor generate fresh keys on first start.
- Preserved identity: back up keys, then restore them on a new install *before* Tor starts.

## Important safety rules

- Treat Tor identity data as sensitive: it can correlate installations over time.
- Never commit plaintext identity archives, vault passwords, host inventories, fingerprints, contact info, onion addresses, or provider IDs.
- This public repo intentionally ships **no** real inventory; copy `inventory.example/` to a private `inventory/` (gitignored) first.

## Backup workflow

Use `ops/tor_identity_backup.yml`.

What it does (high level):
- On each target relay: archives `/var/lib/tor/keys` (plus optional `pt_state`/`fingerprint` if present).
- Fetches archives to your controller.
- Encrypts them with Ansible Vault.
- Removes plaintext staging artifacts.

Where output goes in this template:
- Local staging: `.local/tor_identity/stage/`
- Vaulted output: `.local/tor_identity/vaulted/`

Both locations are gitignored by default.

Example run:

```bash
env -u ANSIBLE_VAULT_PASSWORD_FILE \
  ansible-playbook -i inventory/hosts.ini ops/tor_identity_backup.yml \
  --limit tor_relays
```

## Restore workflow

Restoring identity is implementation-specific (it depends on how your Tor role/container is started).

Typical approach:
- Decrypt the vaulted archive for the host.
- Place extracted keys under the correct Tor DataDirectory on the target.
- Ensure correct ownership/permissions.
- Start Tor.

If you want, I can port your Tor role/playbook next and keep the identity-restore steps generic and opt-in.

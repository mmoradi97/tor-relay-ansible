# tor-relay-ansible

Sanitized, public-safe Ansible project for managing Tor relay infrastructure.

## What’s included
- Roles/playbooks structure (this repo is intentionally seeded without any real inventory).
- Example inventory templates under `inventory.example/`.

## What’s *not* included
- Any real servers, IPs, hostnames, SSH details, Tor contact metadata, relay fingerprints, or anything that can be used to identify or locate an operator.

## Usage
1. Create your private inventory directory:
   - `cp -R inventory.example inventory`
2. Edit files in `inventory/` to match your own infrastructure.
3. Run Ansible using your private `inventory/`.

## Safety notes
- Keep `inventory/` private.
- Use Ansible Vault and/or environment variables for secrets.
- Never commit private keys, API tokens, onion addresses, relay fingerprints, or provider identifiers.

## License
MIT (see `LICENSE`).

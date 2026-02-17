# App toggles (enable/disable)

This public repo supports per-group and per-host toggles that control whether each app should be installed or removed on the next run.

## Variables

- `app_tor_enabled`
- `app_snowflake_enabled`
- `app_conduit_enabled`

## Where to set them

Ansible variable precedence gives you the control model you want:

- Defaults for the whole fleet: `inventory/group_vars/all/app_toggles.yml`
- Desired policy per group: `inventory/group_vars/<group>/app_toggles.yml` (example groups include `tsc` and `sc`)
- Override a single host: create `inventory/host_vars/<host>/app_toggles.yml` (host vars override group vars)

## How it behaves

These toggles are declarative.

- If an app is enabled (`true`), the role converges the host to the installed/running state.
- If an app is disabled (`false`), the role converges the host to an absent state (hard remove).

"Hard remove" means the role will remove what it manages, not only stop it.

## What “hard remove” does

Exact details are role-specific, but in general:

- Conduit (`app_conduit`): removes the Docker container, removes its named volume, and tries to remove the image.
- Snowflake (`app_snowflake`): brings the compose stack down, removes volumes/images, and deletes the project directory.
- Tor (`app_tor`): stops/disables the `tor` service, removes packages and repo configuration, and deletes `/etc/tor` and `/var/lib/tor` (including identity).

## Common workflows

### Remove Conduit from `tsc`

1) Ensure `app_conduit_enabled: false` for the `tsc` group (or override per-host).
2) Run the Conduit playbook limited to the `tsc` group.
3) If you want to avoid baseline roles while doing this, skip dependency tag `deps`.

Example:

```bash
ansible-playbook -i inventory/hosts.ini playbooks/conduit.yml \
  --limit tsc --skip-tags deps
```

### Override a single host

Create a host override file:

```yaml
# inventory/host_vars/tor_relay_pl/app_toggles.yml
app_snowflake_enabled: false
```

Then run the corresponding playbook against that host:

```bash
ansible-playbook -i inventory/hosts.ini playbooks/snowflake.yml \
  --limit tor_relay_pl
```

## Notes

- Because disabled means uninstall, be careful when running playbooks against `hosts: all` without `--limit`.
- If a host is unreachable, it will keep its current state until it becomes reachable and you rerun the playbook.

# Port status

All task files referenced by `tasks/main.yml` are now ported:
- tasks/ssh.yml
- tasks/ufw.yml
- tasks/fail2ban.yml

Safety notes:
- UFW always allows the configured SSH port and the current Ansible connection port to reduce lockout risk.
- Define any additional allow rules in your private `inventory/`.

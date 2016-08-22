# Setup a secure Ubuntu Xenial VPS using Ansible
This playbook defines a single role called `security` which sets up
- ufw
- fail2ban
- unattended-upgrades
- monit

## Securing SSH Access
Installs `ufw` and sets the firewall to deny all, with an exception for SSH traffic on port 22. 

Updates `/etc/ssh/sshd_conf` to disable password authentication and root login.

Installs `fail2ban` with default settings.

## Automatic Security Updates
Installs `unattended-upgrades` with minimal settings.

## Logging SSH Access
Installs `'monit` and updates the update interval to 5 seconds.

Adds a rule which checks for `Accepted publickey` in the log file `'/var/log/auth.log`. If the rule fires, it runs a script which posts server name, user name, and source IP to Slack. 


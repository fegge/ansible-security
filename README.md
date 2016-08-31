# Setup a secure Ubuntu VPS using Ansible
This playbook defines a single role called `security` which sets up
- `ufw`
- `fail2ban`
- `unattended-upgrades`
- SSH logging using `monit`

## Securing SSH Access
Installs `ufw` and sets the firewall to deny all, with an exception for SSH traffic on port 22. 

Updates _/etc/ssh/sshd_conf_ to disable password authentication and root login.

Installs `fail2ban` with default settings.

## Automatic Security Updates
Installs `unattended-upgrades` with minimal settings and adds `Ubuntu {{ ansible_distribution_release }}-security` to allowed origins.

## Logging SSH Access
Installs `monit` and sets the update interval to 5 seconds.

Adds a rule which checks for `Accepted publickey` in the log file _/var/log/auth.log_. If the rule fires, it runs a script which posts server name, user name, and source IP to Slack.

## Role Variables
- `slack_webhook`: Needed to post SSH logins to Slack. Defined in _defaults/main.yml_ and defaults to the empty string. (If the default is not overridden SSH logging is disabled.)

## Example Playbook

    - hosts: all
      roles:
        - role: fegge.security
          slack_webhook: URL

## License
Unlicense (http://unlicense.org).

# Build status
[![Build Status](https://travis-ci.org/fegge/ansible-security.svg?branch=master)](https://travis-ci.org/fegge/ansible-security)

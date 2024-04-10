Common
=========

Handles the process of configuring the SSH service for the system. The SSH service
is commonly utilized for administration aspects of the system and thus represents
something that should be secured.

This role will handle the setup of the ssh daemon and fail2ban to detect and
respond to repeated authentication attempts. Too many failed attempts will trigger
a fail2ban firewall update.

Requirements
------------

Playbook including this role must be executed with elevated privilges.

Role Variables
--------------

There are a few configurable parameter for this role in the system.

| Name | Default | Description |
| ------|-----------|-----------|
| user | admin | Defines name of account to create and provide access to. |
| ssh_authorized_keys | Empty | List of public keys that should be added to authorized_keys for the user |
| ssh_port | 22 | Port on which SSH should listen |
| permit_ssh_password_login | yes | System accepts password for ssh authentication in addition to private/public key |


Example Playbook
----------------

The following is an example use of this role to setup an account called cameron
on a system. This particular setup will also not allow password based authentication
on the system at it's completion.

```
- hosts: local
  become: true
  roles:
    - configure_ssh
  vars:
    user: "cameron"
    permit_ssh_password_login: "no"
    ssh_authorized_keys:
      - "ssh ..."
```      

License
-------

BSD

Author Information
------------------

Cameron Whipple <cameron@starkcybercorp.net>

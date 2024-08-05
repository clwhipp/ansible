# Ansible Host Setup

# Server Setup and Bootstrap

Ansible provides a solution and framework through which maintenance
and setup of infrasture is possible. However, there is a bootstrap
process that is necessary with new machines. By default, ansible
will want to utilize public key authentication for accessing the
machines that are being configured. This does not work before
a machine has been bootstrapped.

The section of the README briefly discusses the process for
bootstrapping a machine.

## Machine Preparation

The preparation process for the target machine mostly relates
to installation of the OS. The process for installing the OS
is beyond scope of this readme. There are a few items that need
to be done as part of that process to make the setup process with
ansible possible.

1. Setup user account with known password (more on this later)
2. Enable SSH access to the system

As far as the user account, the account will be replaced or modified
as part of the bootstrapping process. The account is to allow the ansible
host to login and perform operations as required. Ansible functions through
logging into devices via SSH and performing operations.

Once configured, login to the machine and make note of it's IP address and
ensure that firewalls are open to SSH access by the ansible host.

## Bitwarden Setup

The ansible process utilizes the Bitwarden CLI for pulling passwords and
other secret information during the process. By default, the ansible process
will try to pull the username and password for the servers from Bitwarden. A unique
password is utilized for each server as a means to enforce leave privilege. As such,
it is necessary to setup the appropriate accounts with the Bitwarden account
being utilized for ansible operations.

The naming convention for these accounts within Bitwarden is <host>\_linux_user_password.
The following examples shows the process of pulling the account password for a host
called nexus.

```
ansible_become_pass: "{{ lookup('bitwarden_password', 'nexus_linux_user_password') }}"
user_password: "{{ lookup('bitwarden_field', 'hash', 'nexus_linux_user_password') }}"
```

The first line in the above example is pulling the raw password that enables ansible
to obtain root when working with this particular host. As such, the user account must
be in the sudo group. The second entry is utilized during the bootstrap process for
configuring the password for the account. Recall that the account are using a password
that was configured at OS installation. So, the first thing ansible does is replace
that password with the one within Bitwarden. The ansible module for changing the password
requires the SHA512 digest of the password to be available for this operation.

The following command should be utilized for obtaining the hash. Then, the hash should
be added to the <host>\_linux_user_password entry as an additional field called 'hash'.
This will make the hash available to ansible.

```bash
mkpasswd --method=sha-512 <password>
```

It's also worth noting that there are likely many other passwords and secrets that
will need to be configured within Bitwarden to make this possible.

## Update Inventory

The inventory contains the list of all hosts within the ansible environment. The new
machine will needed to be added to the inventory so that ansible is aware of it. The
inventory can be found within the inventory directory. An entry will need to be added
along with the IP address noted earlier after the OS setup.

The following are examples of entries. The IP address does not need to come from a
vault if not desired.

```
[servers]
nexus ansible_host="{{ nexus_ip_address }}"
warden ansible_host="{{ warden_ip_address }}"
```

In addition, a host_vars file will need to be created for that machine as well. The host_vars
file will contain the host specific variables that ansible requires to operate. For instance,
the host_vars file contains the commands that allow for pulling device specific passwords for
elevating permissions to root.

## Run Bootstrap

After Bitwarden setup, the next step is to run the bootstrap process to prepare
the machine for continued management through ansible. The bootstrap process will
configure the administrative user account, setup public key authentication for SSH,
and change out the users password to be consistent with Bitwarden.

```bash
./bootstrap-host.sh <desired setup playbook> <hostname>
```

The bootstrap-host.sh script will facilitate the entry of a password and enable
password based SSH into the device for the first time until public key authentication
an be handled. After that, the specified playbook will be ran using the passwords
from Bitwarden for the subsequent operations.
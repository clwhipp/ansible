#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <playbook_name> <host_name>"
    exit 1
fi

playbook=$1
hostname=$2

# Prompt the user for the ansible become password
read -s -p "Enter current password: " become_pass
echo

# Run playbook to setup account and password
ansible-playbook "bootstrap.yml" -l "$hostname" --extra-vars "ansible_become_pass=$become_pass ansible_ssh_pass=$become_pass"
unset become_pass

# Run playbook to setup rest of the host
ansible-playbook $playbook

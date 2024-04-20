#!/bin/bash

function install_software(){

    # Install Ansible
    sudo apt update
    sudo apt install software-properties-common unzip
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt -y install ansible sshpass

    # Install Bitwarden CLI
    unzip bw-linux-2024.3.1.zip
    sudo mv bw /usr/bin
    sudo chown root:root /usr/bin/bw
    sudo chmod 755 /usr/bin/bw

}

install_software

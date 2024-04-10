#!/bin/bash

function install_software(){

    # Add necessary PPA's
    sudo add-apt-repository ppa:phoerious/keepassxc

    # Add desired packages
    sudo apt update
    sudo apt install wget gpg keepassxc unzip

    # Install Ansible
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt -y install ansible
}

install_software

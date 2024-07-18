#!/bin/bash

function install_ansible(){
    sudo apt update
    sudo apt install software-properties-common unzip
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt -y install ansible sshpass
}

function install_software(){
    sudo apt install vim
    sudo snap install bw
    sudo snap install bitwarden
}

install_ansible
install_software

- hosts: nexus
  become: true
  roles:
    - configure_nebula

  vars:
    nebula_inject_keys: false
    nebula_package_install: false
    nebula_service_restart: true

  vars_files: 
    - ../vars/env-secrets.yml

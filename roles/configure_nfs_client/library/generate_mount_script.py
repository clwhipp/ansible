#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import yaml
import os

def update_mount_script(script_location, server_addr, share_name, mount_point):

    file_mode = 'w' if not os.path.exists(script_location) else 'a'
    with open(script_location, file_mode) as script_file:
        command = "sudo mount -t nfs4 %s:%s %s\n" % (server_addr, share_name, mount_point)
        script_file.write(command)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            server_addr=dict(type='str', required=True),
            share_name=dict(type='str', required=True),
            mount_point=dict(type='str', required=True),
            mount_script=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    server_address = module.params['server_addr']
    share_name = module.params['share_name']
    mount_point = module.params['mount_point']
    script_location = module.params['mount_script']

    if module.check_mode:
        module.exit_json(changed=False)

    update_mount_script(script_location, server_address, share_name, mount_point)
    module.exit_json(changed=True)

if __name__ == '__main__':
    main()

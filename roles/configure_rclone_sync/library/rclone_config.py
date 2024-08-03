#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os
import configparser

def update_rclone_config(target, access_key_id, secret_access_key):

    rclone_config_loc = '/root/.config/rclone/rclone.conf'
    if not os.path.exists(rclone_config_loc):
        os.makedirs(os.path.dirname(rclone_config_loc))
        os.system('touch ' + rclone_config_loc)

    config = configparser.ConfigParser()
    config.read(rclone_config_loc)

    if target not in config:
        config[target] = {
            'type': 's3',
            'provider': 'IDrive',
            'acl': 'private',
            'endpoint': 'e7u1.ch.idrivee2-26.com',
            'access_key_id': '',
            'secret_access_key': ''
        }

    config[target]['access_key_id'] = access_key_id
    config[target]['secret_access_key'] = secret_access_key

    with open(rclone_config_loc, 'w') as f:
        config.write(f)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            idrive_e2_target=dict(type='str', required=True),
            idrive_e2_access_key_id=dict(type='str', required=True),
            idrive_e2_secret_access_key=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    idrive_e2_target = module.params['idrive_e2_target']
    idrive_e2_access_key_id = module.params['idrive_e2_access_key_id']
    idrive_e2_secret_access_key = module.params['idrive_e2_secret_access_key']

    if module.check_mode:
        module.exit_json(changed=False)

    try:
        update_rclone_config(idrive_e2_target, idrive_e2_access_key_id, idrive_e2_secret_access_key)
        module.exit_json(changed=True)
    except Exception as e:
        module.fail_json(msg="Error updating YAML file: {}".format(e))

if __name__ == '__main__':
    main()

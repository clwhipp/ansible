#!/usr/bin/python

# WIP: Encountered an error when initial use of this was attempted.

from ansible.module_utils.basic import AnsibleModule
import os
import subprocess
import json

def update_attachment(name, file_path):

    cmd = ['bw', 'get', 'item', name]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return False, 'Error fetching item data for {}: {}'.format(name, e.stderr)

    base_name = os.path.basename(file_path)
    item_uid = response['id']

    # Check if item currently exists and delete if so
    for attachment in  response['attachments']:
        if base_name == attachment['fileName']:
            try:
                cmd = ['bw', 'delete', 'attachment', attachment['id'], '--itemid', item_uid]
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                return False, 'Error deleting existing attachment for {}: {}'.format(base_name, e.stderr)

    # create new item to track new state
    try:
        cmd = ['bw', 'create', 'attachment', '--file', file_path, '--itemid', item_uid]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return False, 'Error creating attachment for {}: {}'.format(base_name, e.stderr)

    return True, ''

def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            file_path=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    name = module.params['name']
    file_path = module.params['file_path']

    if module.check_mode:
        module.exit_json(changed=False)

    result, message = update_attachment(name, file_path)
    if not result:
        module.fail_json(msg="Error updating attachment: {}".format(message + str(os.getuid())))
    else:
        module.exit_json(changed=True)

if __name__ == '__main__':
    main()

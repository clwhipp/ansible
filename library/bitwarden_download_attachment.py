#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess
import json

def download_single_attachment(name, filename, file_path):

    cmd = ['bw', 'get', 'item', name]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return False, 'Error fetching item data for {}: {}'.format(name, e.stderr)

    item_uid = response['id']
    cmd = ['bw', 'get', 'attachment', filename, '--itemid', item_uid, '--output', file_path]
    try:
        download_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return False, 'Error downloading attachment {}: {}'.format(filename, e.stderr)
                    
    return True, ''


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            filename=dict(type='str', required=True),
            file_path=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    name = module.params['name']
    filename = module.params['filename']
    file_path = module.params['file_path']

    if module.check_mode:
        module.exit_json(changed=False)

    result, message = download_single_attachment(name, filename, file_path)
    if not result:
        module.fail_json(msg="Error downloading attachments: {}".format(message + str(os.getuid())))
    else:
        module.exit_json(changed=True)

if __name__ == '__main__':
    main()

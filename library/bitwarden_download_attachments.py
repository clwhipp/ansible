#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess
import json

def download_attachments(name, dir_path):

    cmd = ['bw', 'get', 'item', name]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return False, 'Error fetching item data for {}: {}'.format(name, e.stderr)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    item_uid = response['id']
    for attachment in  response['attachments']:

        fileName = attachment['fileName']
        output_location = os.path.join(dir_path, fileName)
        cmd = ['bw', 'get', 'attachment', fileName, '--itemid', item_uid, '--output', output_location]
        try:
            download_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return False, 'Error download attachment {}: {}'.format(fileName, e.stderr)

        if download_result.returncode != 0:
            return False, 'Error fetching secret for {}: {}'.format(name, e.stderr)
                           
    return True, ''


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            dir_path=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    name = module.params['name']
    dir_path = module.params['dir_path']

    if module.check_mode:
        module.exit_json(changed=False)

    result, message = download_attachments(name, dir_path)
    if not result:
        module.fail_json(msg="Error downloading attachments: {}".format(message + str(os.getuid())))
    else:
        module.exit_json(changed=True)

if __name__ == '__main__':
    main()

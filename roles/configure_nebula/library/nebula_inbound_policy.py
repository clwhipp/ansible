#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import yaml
import os

def yaml_update(file_path, rules):

    with open(file_path, 'r') as file:
        yaml_config = yaml.safe_load(file)

    inbound_entries = []
    for item in rules:
        entry = {}
        entry['port'] = item['port']
        entry['proto'] = item['proto']
        entry['group'] = item['group']
        inbound_entries.append(entry)

    yaml_config['firewall']['inbound'] = inbound_entries

    # Write back to the YAML file
    with open(file_path, 'w') as file:
        yaml.safe_dump(yaml_config, file, default_flow_style=False)

    return True

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            rules=dict(type='list', required=True),
        ),
        supports_check_mode=True
    )

    path = module.params['path']
    rules = module.params['rules']

    if not os.path.exists(path):
        module.exit_json(changed=False, message="No Configuration file found at " + path + "!")

    if module.check_mode:
        module.exit_json(changed=False)

    try:
        yaml_update(path, rules)
        module.exit_json(changed=True)
    except Exception as e:
        module.fail_json(msg="Error updating YAML file: {}".format(e))

if __name__ == '__main__':
    main()

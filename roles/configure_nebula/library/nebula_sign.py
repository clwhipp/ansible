#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import os
import yaml
import json
import base64
from datetime import datetime

class Address(object):

    def __init__(self, cidr_format = None):
        self._address = '0.0.0.0'
        self._subnet = '24'
        self._last_octet = '0'
        self._process_address(cidr_format)

    def _process_address(self, cidr_format):

        if cidr_format == None:
            return

        l1_splits = cidr_format.split('/')
        if len(l1_splits) != 2:
            return

        self._subnet = l1_splits[1]
        self._address = l1_splits[0]
        addr_splits = self._address.split('.')
        self._last_octet = addr_splits[3]

    @property
    def address(self):
        return self._address

    @property
    def octet(self):
        return self._last_octet

    @property
    def mask(self):
        return self._subnet

    def __str__(self):

        if self.address is None or self.mask is None:
            return ''

        address = self.address
        if address is None:
            address = ''

        mask = self.mask
        if mask is None:
            mask = ''

        return address + '/' + mask

class NebulaCertificate(object):

    def __init__(self, path, executable=r'nebula-cert'):
        self._path = path
        self._exe = executable

        self._name = ''
        self._start_time = None
        self._expire_time = None
        self._public = None
        self._public_encoded = None
        self._groups = []
        self._address = Address(None)
        self._fingerprint = None
        self._signature = None
        self._issuer = None

        self._perform_extraction(path)

    def _perform_extraction(self, file_path):

        cmd = [self.exe, 'print', '-json', '-path', file_path]
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)

        # Access the captured stdout
        captured_stdout = completed_process.stdout
        cert_data = json.loads(captured_stdout)
        details = cert_data['details']

        self._name = details['name']
        self._start_time = details['notBefore']
        self._expire_time = details['notAfter']
        self._public = bytes.fromhex(details['publicKey'])
        self._public_encoded = base64.b64encode(self._public).decode('utf-8')
        self._groups = details['groups']
        if(len(details['ips']) > 0):
            self._address = Address(details['ips'][0])
        self._fingerprint = cert_data['fingerprint']
        self._signature = cert_data['signature']
        self._issuer = details['issuer']

    @property
    def exe(self):
        return self._exe

    @exe.setter
    def exe(self, value):
        self._exe = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def expiration_string(self):
        return self._expire_time

    @expiration_string.setter
    def expire_time(self, value):
        self._expire_time = value

    @property
    def issuance(self):
        return datetime.strptime(self._start_time, "%Y-%m-%dT%H:%M:%S%z")

    @property
    def expiration(self):
        return datetime.strptime(self.expiration_string, "%Y-%m-%dT%H:%M:%S%z")

    @property
    def public(self):
        return self._public

    @public.setter
    def public(self, value):
        self._public = value

    @property
    def public_encoded(self):
        return self._public_encoded

    @public_encoded.setter
    def public_encoded(self, value):
        self._public_encoded = value

    @property
    def fingerprint(self):
        return self._fingerprint

    @fingerprint.setter
    def fingerprint(self, value):
        self._fingerprint = value

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value

    @property
    def ipv4_address(self):
        return self._address

    @ipv4_address.setter
    def ipv4_address(self, value):
        self._address = value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, value):
        self._signature = value

    @property
    def issuer(self):
        return self._issuer

    @issuer.setter
    def issuer(self, value):
        self._issuer = value

    def exportNebulaPublic(self, location):
        with open(location, 'w') as f:
            f.write('-----BEGIN NEBULA X25519 PUBLIC KEY-----\n')
            f.write(self.public_encoded + '\n')
            f.write('-----END NEBULA X25519 PUBLIC KEY-----\n')

    def __str__(self):
        return self.name + " with public " + self.public_encoded

def sign_cert(profile, config, ca_key, ca_key_pass, ca_crt, public, out_crt):

    if not os.path.exists(config):
        return False, "Cert configuration couldn't be found at " + config
    
    with open(config, 'r') as file:
        yaml_config = yaml.safe_load(file)

    if profile not in yaml_config:
        return False, profile + " profile was not found in " + config

    dir_name = os.path.dirname(out_crt)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if os.path.exists(out_crt):
        os.remove(out_crt)
    
    device_profile = yaml_config[profile]

    dev_name = profile
    dev_grps_csv = ','.join(device_profile['groups'])
    dev_ip = device_profile['vpn_ip']
    dev_duration = device_profile['validity']

    cmd = ['nebula-cert', 'sign', '-ca-crt', ca_crt, '-ca-key', ca_key, '-ca-key-pass', ca_key_pass, '-duration', dev_duration, '-groups', dev_grps_csv, '-in-pub', public, '-ip', dev_ip, '-name', dev_name, '-out-crt', out_crt]
    try:
        # Issue the certificate with private keys
        subprocess.run(cmd, check=True)

        # Extract attributes from certificate to update logs
        cert = NebulaCertificate(out_crt)
        entry = {}
        entry['issue_date'] = cert.issuance
        entry['expiration'] = cert.expiration
        entry['fingerprint'] = cert.fingerprint
        entry['groups'] = dev_grps_csv

        yaml_config[profile]['public'] = cert.public_encoded
        if 'certs' not in yaml_config[profile]:
            yaml_config[profile]['certs'] = []
        yaml_config[profile]['certs'].append(entry)

        # Write out the updated configuration with logs
        with open(config, 'w') as file:
            yaml.dump(yaml_config, file, default_flow_style=False, sort_keys=False)

    except subprocess.CalledProcessError as e:
        return False, str(e)

    return True, ''


def main():
    module_args = dict(
        profile=dict(type='str', required=True),
        config=dict(type='str', required=True),
        ca_key=dict(type='str', required=True),
        ca_key_pass=dict(type='str', required=True),
        ca_crt=dict(type='str', required=True),
        public=dict(type='str', required=True),
        out_crt=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    profile = module.params['profile']
    config = module.params['config']
    ca_key = module.params['ca_key']
    ca_key_pass = module.params['ca_key_pass']
    ca_crt = module.params['ca_crt']
    public = module.params['public']
    out_crt = module.params['out_crt']

    if module.check_mode:
        module.exit_json(**result)

    success, error = sign_cert(profile, config, ca_key, ca_key_pass, ca_crt, public, out_crt)

    if success:
        result['changed'] = True
        result['message'] = "Successfully generated devices certificate from profile"
        module.exit_json(**result)
    else:
        module.fail_json(msg=f"Failed to generate devices certificate: {error}")

if __name__ == '__main__':
    main()

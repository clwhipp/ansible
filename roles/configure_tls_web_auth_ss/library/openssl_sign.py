from ansible.module_utils.basic import AnsibleModule
import subprocess
from datetime import datetime

def sign_cert(csr_path, ca_key, ca_crt, tls_ext, out_crt):

    cmd = ['openssl', 'x509', '-req', '-in', csr_path, '-CA', ca_crt, '-CAkey', ca_key, '-CAcreateserial', '-out', out_crt, '-days', '400', '-sha256', '-extfile', tls_ext]
    try:
        # Issue the certificate with private keys
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        return False, str(e)

    return True, ''

def main():
    module_args = dict(
        csr_path=dict(type='str', required=True),
        ca_key=dict(type='str', required=True),
        ca_crt=dict(type='str', required=True),
        tls_ext=dict(type='str', required=True),
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

    csr_path = module.params['csr_path']
    ca_key = module.params['ca_key']
    ca_crt = module.params['ca_crt']
    tls_ext = module.params['tls_ext']
    out_crt = module.params['out_crt']

    if module.check_mode:
        module.exit_json(**result)

    success, error = sign_cert(csr_path, ca_key, ca_crt, tls_ext, out_crt)

    if success:
        result['changed'] = True
        result['message'] = "Successfully generated devices certificate from profile"
        module.exit_json(**result)
    else:
        module.fail_json(msg=f"Failed to generate devices certificate: {error}")

if __name__ == '__main__':
    main()
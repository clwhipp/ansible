from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import subprocess
import json

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        secrets = []

        if len(terms) < 2:
            raise AnsibleError('This lookup requires a field and a name')
        
        target_field=terms[0]
        target_name=terms[1]

        cmd = ['bw', 'get', 'item', target_name]
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            response = json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise AnsibleError('Error fetching secret for {}: {}'.format(target_name, e.stderr))
        
        for field in response['fields']:
            if field['name'] == target_field:
                secrets.append(field['value'])

        return secrets

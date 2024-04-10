from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import subprocess

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        secrets = []
        for term in terms:
            cmd = ['bw', 'get', 'password', term]
            try:
                result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                secrets.append(result.stdout)
            except subprocess.CalledProcessError as e:
                raise AnsibleError('Error fetching secret for {}: {}'.format(term, e.stderr))

        return secrets

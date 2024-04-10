# Ansible Vault

The ansible vaults are utilized to store meta-data that is considered to be sensitive. With this design, the storage
of passwords and keys is contained to Bitwarden. The ansible vaults are not utilized to store those passwords within
these roles and playbooks.

The following is an example dump of the contents of the env-secrets.yml in this repo. This shows the content
necessary to fill in to be compatible with the roles. The use of the *_v is utilized as a convention to indicate
that value is pulled from the vault within the roles.

```yaml
user_v: ""
user_uid_v: ""
domain_v: "domain.tld"
nebula_port_v: <port>
ssh_authorized_keys_v:
  - "<key 1>"
  - "<key 2>"
  - "<key 3>"
root_install_dir_v: "/opt/admin"

# Certificate Signing Request - TLS Certificate Issuance
csr_country_v: "US"
csr_state_v: "State"
csr_city_v: "City"
csr_org_v: "Organization name"

# Nextcloud Settings
nextcloud_db_user_v: "account a"
nextcloud_admin_user_v: "admin account b"

# NFS Settings
nfs_server_ip_v: "10.30.0.1"

# Misc
admin_repo_url_v: "git@github.com:..."
```
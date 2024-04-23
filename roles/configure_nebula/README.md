Nebula VPN
=========

The Nebula VPN is an open-source VPN that utilizes certificates to represent devices
within the network. Each device in the network receives a unique identity with the
appropriate bind groups, or labels, to each of those devices. These groups or labels
can then be utilized with firewall policies on servers to restrict access to resources.

This role utilizes an issuance-profiles.yml file that is downloaded from Bitwarden
as a means to determine what attributes to add to the certificate. The issuance-profiles.yml
comprises of a list of profiles and a lookup is performed during execution

```yaml
devicea.domain.net:
  groups:
  - version:2
  - net:net-name
  - os:ios
  - form:phone
  - acl:appA
  public: <public key here>
  validity: 8760h
  vpn_ip: 1.2.3.5/24
server.domain.net:
  groups:
  - version:2
  - net:net-name
  - os:linux
  - form:server
  - acl:nfs
  public: <public key here>
  validity: 9000h
  vpn_ip: 1.2.4.6/24
windows.domain.net:
  groups:
  - version:2
  - net:net-name
  - os:windows
  - form:laptop
  - acl:nextcloud
  public: <public key here>
  validity: 8000h
  vpn_ip: 1.2.3.8/24
```

These will allow the role to generate certificates with appropriate attribution. Then, the resource
servers can be secured using firewall access policies that inspect those attributes. For instance,
the following access policy would allow administrative devices to access ssh. The example also
would allow devices in an "acl:nextcloud" group to have access to port 443.

```
nebula_inbound_rules:

  - port: "{{ ssh_port }}"
    proto: tcp
    group: acl:admin

  - port: 443
    proto: tcp
    group: acl:nextcloud

```

This combination of attribution in certificates and creation of access policies enable
a capability to manage access to network resources.

Requirements
------------

The use of Nebula VPN requires that a lighthouse server is stood up and maintained. The lighthouse
acts as a coordination server between members of the nebula network. This means that it enables
various devices (phones, tablets, computers, servers) to find each other regardless of their
physical IP address.

Role Variables
--------------


Dependencies
------------


Example Playbook
----------------

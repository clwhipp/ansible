#!/bin/bash

update_ca_path() {
    if [ -z "${NODE_EXTRA_CA_CERTS}" ]; then
        ca_path="$(pwd)/ca.crt"
        echo "Setting NODE_EXTRA_CA_CERTS to $ca_path"
        export NODE_EXTRA_CA_CERTS=$ca_path
    fi
}

update_ca_path
export BW_SESSION=$(bw unlock --raw)

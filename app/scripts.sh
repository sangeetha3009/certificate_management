#!/bin/bash

# Bash shell script for generating self-signed certs. Run this in a folder, as it
# generates a few files. Large portions of this script were taken from the
# following artcile:
# 
# http://usrportage.de/archives/919-Batch-generating-SSL-certificates.html
# 
# Additional alterations by: Brad Landers
# Date: 2012-01-27

# Script accepts a single argument, the fqdn for the cert
DOMAIN="$1"
CERTNO="$4"
if [ -z "$DOMAIN" ]; then
  echo "Usage: $(basename $0) <domain>"
  exit 11
fi

fail_if_error() {
  [ $1 != 0 ] && {
    unset PASSPHRASE
    exit 10
  }
}

# Generate a passphrase
export PASSPHRASE=$(head -c 500 /dev/urandom | tr -dc a-z0-9A-Z | head -c 128; echo)

# Certificate details; replace items in angle brackets with your own info
subj="
O=$3
commonName=$DOMAIN
emailAddress=$2
days="1"
"

# Generate the server private key
openssl genrsa -des3 -out $CERTNO.key -passout env:PASSPHRASE 2048
fail_if_error $?

# Generate the CSR
openssl req \
    -new \
    -batch \
    -subj "$(echo -n "$subj" | tr "\n" "/")" \
    -key $CERTNO.key \
    -out $CERTNO.csr \
    -passin env:PASSPHRASE
fail_if_error $?
cp $CERTNO.key $CERTNO.key.org
fail_if_error $?

# Strip the password so we don't have to type it every time we restart Apache
openssl rsa -in $CERTNO.key.org -out $CERTNO.key -passin env:PASSPHRASE
fail_if_error $?

# Generate the cert (good for 1 day)
openssl x509 -req -days 1 -in $CERTNO.csr -signkey $CERTNO.key -out $CERTNO.crt
fail_if_error $?

exit 0

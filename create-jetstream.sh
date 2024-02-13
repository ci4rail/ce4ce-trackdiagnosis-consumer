#! /bin/bash

# Ensure you are using the "NGS NATS Agilis Pilot" account
# https://vault.bitwarden.com/#/vault?search=ngs&itemId=08d8fd01-725c-41a6-a4bf-afee0083ce82

nats stream create ce4ce-track-sim --subjects "TRACKSIM.>" --storage file --max-bytes=10M --retention limits --replicas 3 --discard old

# add user
nsc add user --name cemit --allow-pubsub "TRACKSIM.>"
nsc push

# generate creds
nsc generate creds --name cemit
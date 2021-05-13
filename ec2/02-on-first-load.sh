#!/bin/bash

# Start docker service
sudo service docker start



# setup Janis with CWLTool
mkdir -p ~/janis-portable-pipeline && cd ~/janis-portable-pipeline

mkdir -p ~/.janis/
cat <<EOT >> ~/.janis/janis.conf
engine: cwltool
notifications:
  email: null
template:
  id: local
EOT

# Download data

wget -q -O- "https://github.com/PMCC-BioinformaticsCore/janis-workshops/raw/master/bcc2020/resources/bcc-data.tar" \
    | tar -xz

# Allow password login
sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config
sudo service sshd restart

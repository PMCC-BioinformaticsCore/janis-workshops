#!/bin/bash

# Start docker service
sudo service docker start

# Allow password login
sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config
sudo service sshd restart
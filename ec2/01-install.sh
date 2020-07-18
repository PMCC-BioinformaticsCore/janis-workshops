#!/bin/bash

sudo yum update -y
sudo yum install -y yum-utils

# Install Docker and add user to docker group
sudo amazon-linux-extras install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Python + gcc (required for some packages)
sudo yum install -y python3 gcc python3-devel

# Install Janis
pip3 install --user janis-pipelines

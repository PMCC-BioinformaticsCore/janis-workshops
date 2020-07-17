keyname=$1
keypath=$2
participant=$3

__dir=$(dirname $0)

password=$(python3 $__dir/pwgen.py)

instanceID=$(aws ec2 run-instances \
    --image-id ami-0a58e22c727337c51 \
    --count 1 --instance-type t2.large \
    --key-name $keyname \
    --query 'Instances[0].InstanceId' --output text \
    --tag-specification "ResourceType=instance,Tags=[{Key=User,Value=$participant},{Key=Project,Value=Janis-workshop-bcc2020}]" \
    --user-data file://$__dir/01-install.sh \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30,"DeleteOnTermination":true}}]' \
    --security-group-ids sg-0c3bb8034f313fac1 \
)

echo $instanceID >> instanceIds.txt

echo "Instance is starting: $instanceID"
aws ec2 wait instance-status-ok --instance-ids $instanceID
echo "Instance has started: $instanceID"

url=$(aws ec2 describe-instances --instance-ids "$instanceID" | jq '.Reservations[0].Instances[0].PublicDnsName')

# ssh -i $keypath -oStrictHostKeyChecking=no $

alias sshtoinstance="ssh -i $keypath -oStrictHostKeyChecking=no ec2-user@$url"

sshtoinstance "echo $password | sudo passwd ec2-user --stdin"

sshtoinstance docker pull biocontainers/bwa:v0.7.15_cv3
sshtoinstance docker pull quay.io/biocontainers/samtools:1.9--h8571acd_11
sshtoinstance docker pull broadinstitute/gatk:4.1.4.0

echo "$participant,ec2-user,$instanceID,$url,$password" >> credentials.txt


keyname=$1
keypath=$2
participant=$3

__dir=$(dirname $0)

password=$(python3 $__dir/pwgen.py)

AMI="ami-08167094da531571a"

# instanceID=$(aws ec2 run-instances \
#     --image-id ami-0a58e22c727337c51 \
#     --count 1 --instance-type t2.large \
#     --key-name $keyname \
#     --query 'Instances[0].InstanceId' --output text \
#     --tag-specification "ResourceType=instance,Tags=[{Key=User,Value=$participant},{Key=Project,Value=Janis-workshop-portable-pipeline}]" \
#     --user-data file://$__dir/01-install.sh \
#     --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30,"DeleteOnTermination":true}}]' \
#     --security-group-ids sg-0c3bb8034f313fac1 \
# )

# Create Janis instance
instanceID=$(aws ec2 run-instances \
    --image-id $AMI \
    --count 1 --instance-type t2.large \
    --key-name $keyname \
    --query 'Instances[0].InstanceId' --output text \
    --tag-specification "ResourceType=instance,Tags=[{Key=User,Value=$participant},{Key=Project,Value=Janis-workshop-bcc2020}]" \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30,"DeleteOnTermination":true}}]' \
    --security-group-ids sg-0c3bb8034f313fac1 \
)

echo $instanceID >> instanceIds.txt

echo "Instance is starting: $instanceID"
aws ec2 wait instance-status-ok --instance-ids $instanceID
echo "Instance has started: $instanceID"

url=$(aws ec2 describe-instances --instance-ids "$instanceID" | jq --raw-output '.Reservations[0].Instances[0].PublicDnsName')
ipaddress=$(aws ec2 describe-instances --instance-ids "$instanceID" | jq --raw-output '.Reservations[0].Instances[0].PublicIpAddress')

alias sshtoinstance="ssh -i $keypath -oStrictHostKeyChecking=no ec2-user@$url"

# SCP requires IP address because I didn't enable some DNS thing
scp -i $keypath -oStrictHostKeyChecking=no $__dir/02-on-first-load.sh ec2-user@$ipaddress:~/
ssh -i $keypath -oStrictHostKeyChecking=no ec2-user@$url 'bash ~/02-on-first-load.sh'
ssh -i $keypath -oStrictHostKeyChecking=no ec2-user@$url "echo $password | sudo passwd ec2-user --stdin"

echo "$participant,ec2-user,$instanceID,$url,$password" >> credentials.txt


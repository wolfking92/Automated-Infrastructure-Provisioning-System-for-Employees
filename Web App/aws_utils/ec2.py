import boto3
from config import (
    AWS_REGION,
    AMI_ID,
    KEY_NAME,
    SECURITY_GROUP_ID,
    MAX_INSTANCES_PER_EMPLOYEE,
    SUBNET_NAME_MAP
)

# ✅ Create EC2 client ONCE
ec2 = boto3.client("ec2", region_name=AWS_REGION)


def get_instances(employee_id):
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:EmployeeID", "Values": [employee_id]},
            {"Name": "instance-state-name", "Values": ["pending", "running", "stopped"]}
        ]
    )

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append({
                "id": instance["InstanceId"],
                "type": instance["InstanceType"],
                "private_ip": instance.get("PrivateIpAddress", "N/A"),
                "subnet_name": SUBNET_NAME_MAP.get(
                    instance["SubnetId"], "Private Subnet"
                )
            })

    return instances


def can_launch_instance(employee_id):
    return len(get_instances(employee_id)) < MAX_INSTANCES_PER_EMPLOYEE


def launch_instance(instance_type, subnet_id, employee_name, employee_id):
    ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=instance_type,
        KeyName=KEY_NAME,
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_id,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "EmployeeName", "Value": employee_name},
                    {"Key": "EmployeeID", "Value": employee_id}
                ]
            }
        ]
    )


def delete_instance(instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])

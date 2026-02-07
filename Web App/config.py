AWS_REGION = "ap-south-1"

AMI_ID = "ami-00ca570c1b6d79f36"      # your AMI
KEY_NAME = "nn"                      # nn.pem
SECURITY_GROUP_ID = "sg-0b37bac2110de937b"

MAX_INSTANCES_PER_EMPLOYEE = 2

SUBNETS = {
    "Private Subnet 1": "subnet-0dc827cee66da6332",
    "Private Subnet 2": "subnet-021adfc4f1e0047be"
}

SUBNET_NAME_MAP = {
    "subnet-0dc827cee66da6332": "Private Subnet 1",
    "subnet-021adfc4f1e0047be": "Private Subnet 2"
}
# Employees Multi-Tier Infrastructure on AWS with Terraform.


A complete Infrastructure implementation for deploying a production-ready, multi-tier architecture on AWS for Employees. This project demonstrates how to build compute and network infrastructure with public and private subnets, load balancing, and enterprise-level security using Terraform.

## What This Project Does

This is a fully automated web app that sets up a complete AWS compute and networking environment from scratch. The infrastructure creates a custom EC2 in private subnets across multiple availability zones, an Application Load Balancer for traffic distribution, and a bastion host for secure SSH access to private resources.

The setup includes proper network isolation – EC2 servers run in private subnets with no direct internet access, while the load balancer sits in public subnets handling all incoming traffic. A NAT Gateway enables private instances to reach the internet for updates while remaining protected from inbound connections.

## Architecture

### AWS Cloud

The infrastructure is deployed in AWS region **ap-south-1** (Mumbai) using the following setup:

**VPC Configuration:**
- VPC Name: `My Vpc 2`
- CIDR Range: `192.168.1.0/24`
- Total Available IPs: 256 addresses

**Subnets Across Two Availability Zones:**

Public Subnets (for load balancer, NAT, and bastion):
- Public Subnet 1: `192.168.1.0/26` in ap-south-1a (62 usable IPs)
- Public Subnet 2: `192.168.1.64/26` in ap-south-1b (62 usable IPs)

Private Subnets (for application servers):
- Private Subnet 1: `192.168.1.128/26` in ap-south-1a (62 usable IPs)
- Private Subnet 2: `192.168.1.192/26` in ap-south-1b (62 usable IPs)

### Network Flow

```
Internet Users
      ↓
Internet Gateway (igw)
      ↓
Application Load Balancer (web-app-albb)
- Listener: HTTP:80
- Forwards to Target Group on port 5000
      ↓
Target Group (app-tg) - Health checks on port 5000
      ↓
EC2 Instances in Private Subnets (Application on port 5000)
- Instance ID: i-0dbd042a041e51117
      ↓
NAT Gateway for outbound internet access
      ↓
Internet Gateway
```

### Bastion Host Access Pattern

```
Your Computer
      ↓
  Git Bash
      ↓
SSH (port 22)
      ↓
Bastion Host in Public Subnet (192.168.1.x)
      ↓
SSH (port 22)
      ↓
Application Instances in Private Subnets
```

## Technology Stack

**Infrastructure as Code:**
- Terraform - Infrastructure automation
- AWS Provider - Cloud resource management

**Cloud Infrastructure:**
- Amazon VPC - Network isolation
- EC2 Instances - t3.micro (2 vCPU, 1 GB RAM)
- Application Load Balancer - Traffic distribution
- NAT Gateway - Secure outbound connectivity
- Internet Gateway - Inbound traffic routing
- Elastic IP - Static IP for NAT Gateway

**Operating System:**
- Amazon Linux 2
- AMI: ami-00ca570c1b6d79f36

## Infrastructure Components

### VPC and Network Setup

The VPC provides complete network isolation with carefully planned CIDR blocks:

```
VPC CIDR: 192.168.1.0/24
├── Public Subnet 1:  192.168.1.0/26    (IPs: .1 to .62)    - AZ: ap-south-1a
├── Public Subnet 2:  192.168.1.64/26   (IPs: .65 to .126)  - AZ: ap-south-1b
├── Private Subnet 1: 192.168.1.128/26  (IPs: .129 to .190) - AZ: ap-south-1a
└── Private Subnet 2: 192.168.1.192/26  (IPs: .193 to .254) - AZ: ap-south-1b
```

**Internet Gateway:**
- Attached to VPC
- Enables communication between VPC and internet
- Used by public subnets for inbound/outbound traffic

**NAT Gateway:**
- Deployed in Public Subnet 1 and Public Subnet 2
- Elastic IP assigned for stable outbound IP
- Allows private instances to initiate outbound connections
- Blocks all inbound connections from internet

### Load Balancer Setup

The Application Load Balancer handles all incoming HTTP traffic:

```
Name: web-app-albb
Type: Application Load Balancer
Scheme: internet-facing
Subnets: Public Subnet 1, Public Subnet 2
Security Group: alb_sg
```

**Listener Configuration:**
```
Protocol: HTTP
Port: 80
Default Action: Forward to app-tg target group
```

**Target Group Configuration:**
```
Name: app-tg
Protocol: HTTP
Port: 5000
Target Type: instance
VPC: My Vpc 2

Health Check:
- Path: /
- Protocol: HTTP
- Port: 5000
- Healthy Threshold: 2 checks
- Unhealthy Threshold: 2 checks
- Timeout: 5 seconds
- Interval: 30 seconds
```

**Target Registration:**
```
Instance ID: i-0dbd042a041e51117
Port: 5000
```

### Security Groups

Three security groups control network access with least-privilege principle:

**alb_sg** - For the Application Load Balancer
```
Inbound Rules:
- HTTP (80) from 0.0.0.0/0 (internet)

Outbound Rules:
- All traffic to 0.0.0.0/0
```

**app_sg** - For Application Instances  
```
Inbound Rules:
- SSH (22) from alb_sg (load balancer security group)

Outbound Rules:
- All traffic to 0.0.0.0/0
```

**web_sg** - For Bastion Host
```
Inbound Rules:
- SSH (22) from 0.0.0.0/0

Outbound Rules:
- All traffic to 0.0.0.0/0
```

### Bastion Host

Secure jump server for SSH access to private instances:

```
Instance Type: t3.micro
AMI: ami-00ca570c1b6d79f36
Availability Zone: ap-south-1a
Subnet: Public Subnet 1
Public IP: Auto-assigned
Key Pair: host1
Security Group: web_sg
```

**Connect to private EC2 instances:**


👩‍💻 EMPLOYEE USER GUIDE
Launching & Accessing Your EC2 Instance (Step-by-Step)
🧩 PART 1: WHAT YOU NEED (ONE TIME ONLY)
Before starting, make sure you have:
Git Bash installed on your laptop
Private key file provided by admin 

TO INSTALL GIT BASH ON YOUR LAPTOP USE THESE LINK:
https://git-scm.com/install/windows

🚀 PART 2: HOW TO LAUNCH AN EC2 INSTANCE (WEB APP)
Step 1️: Open the Web App
Open your browser

Enter the web app URL given by your admin

Step 2️: Login

Enter:
Employee Name
Employee ID
Click Login

✅ You will be redirected to the Dashboard

Step 3️: Launch an EC2 Instance
You will see:
Welcome message with your name
Select Instance Type
Select Subnet (Private Subnet 1 or 2)
Click Launch Instance

⚠️ Important:

You can launch maximum 2 instances


Step 4️: Confirm Instance Launch

After launching, you will see a message box showing:

✅ Instance ID

✅ Instance Type

✅ Subnet Name (Private Subnet 1 or 2)

✅ Private IP Address

✅ Delete button (to terminate instance)

🎉 This means your instance is ready

🔐 PART 3: HOW TO ACCESS YOUR EC2 INSTANCE (VERY EASY)

Step 1️: Open Git Bash
On Windows, open Git Bash
You will see a black terminal window

Step 2️: Create .SSH folder in windows user 

Step 3: Go to SSH Folder (Only First Time)
cd ~/.ssh

(You only do this once)

Step 3️: Connect to Your Instance
Use one of these commands:

👉 To access first instance:
ssh private1

👉 To access second instance:
ssh private2


✅ That’s it.
You are now logged into your private EC2 instance.

🔁 PART 4: IF YOUR INSTANCE IP CHANGES

Sometimes EC2 private IPs change.
If access fails:

Inform admin OR

Update the IP in SSH config file (admin usually does this)

👉 You still use:

ssh private1
ssh private2

🗑 PART 5: HOW TO DELETE YOUR INSTANCE

Open the Dashboard

Find your instance message box

Click Delete

⚠️ This will permanently terminate the instance



### Monthly Costs

**EC2 Instance (Bastion - t3.micro):**
- $0.0146 per hour × 730 hours = **$10.66/month**
- Running 24/7 for SSH access

**Application Instances (t3.micro):**
- $0.0146 per hour × 730 hours = **$10.66/month** per instance
- Launch template allows scaling based on demand

**Application Load Balancer:**
- Fixed: $0.0306 per hour × 730 hours = **$22.34/month**
- LCU charges: **$3-5/month** for moderate traffic
- Includes: 25 new connections/sec, 3000 active connections, 1GB/hour bandwidth

**NAT Gateway:**
- Fixed: $0.065 per hour × 730 hours = **$47.45/month**
- Data processing: $0.065 per GB
- Typical data transfer: **$2-5/month** for moderate usage

**Elastic IP:**
- Free when associated with running instance
- $0.005/hour if not associated = **$3.65/month** (if unused)

**Data Transfer:**
- First 1 GB/month: Free
- Next 10 TB: $0.09 per GB
- Estimated: **$3-8/month** for moderate traffic

**Total Estimated Monthly Cost: $99-117/month**


## What I Learned

Building this Terraform infrastructure taught me important concepts about AWS and Infrastructure as Code:

**Terraform Fundamentals:**
Understanding resource dependencies was crucial. Terraform automatically determines the correct order to create resources - VPC before subnets, subnets before instances, security groups before they're referenced. The dependency graph makes infrastructure deployment reliable and repeatable.

**Network Design:**
CIDR block planning requires careful calculation. Using /26 subnets gives 62 usable IPs per subnet, which is perfect for small to medium deployments. I learned to always reserve the first 4 IPs in each subnet (AWS reserves them for network, gateway, DNS, and future use).

**Security Architecture:**
The principle of least privilege is implemented through security group chaining. Application instances only accept traffic from the ALB and bastion host - never directly from the internet. This defense-in-depth approach adds multiple security layers.

**NAT Gateway vs NAT Instance:**
NAT Gateway is AWS-managed, highly available, and scales automatically but costs $47+/month. NAT Instance requires manual setup and maintenance but costs only $3-4/month. For production, the managed service is worth the premium.

**Resource Tagging:**
Proper tags make resource management much easier. Tags like "Name", "Environment", "Project" help with cost allocation, automation, and identifying resources in the console.

```

## Future Enhancements

1. **HTTPS Support** - Enable secure connections
   - Request SSL certificate from AWS Certificate Manager
   - Add HTTPS listener on ALB port 443
   - Redirect HTTP to HTTPS automatically

2. **Multi-Region Deployment** - Global availability
   - Deploy identical infrastructure in us-east-1
   - Route53 for geographic traffic routing
   - Cross-region VPC peering if needed

3. **Database Layer** - Add persistent storage
   - RDS PostgreSQL or MySQL in private subnets
   - Multi-AZ for high availability
   - Automated backups and snapshots

4. **Monitoring and Logging** - Better observability
   - CloudWatch dashboard for key metrics
   - VPC Flow Logs for network analysis
   - ALB access logs to S3
   - SNS alerts for critical events

5. **Network ACLs** - Additional security layer
   - Subnet-level traffic filtering
   - Deny rules for known malicious IPs




## Contact

If you have questions about this Terraform configuration or want to discuss AWS architecture:

- Email: rahulbaswala73@gmail.com
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)
- GitHub: [your-username](https://github.com/your-username)

---



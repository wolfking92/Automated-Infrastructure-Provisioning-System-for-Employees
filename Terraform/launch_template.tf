resource "aws_launch_template" "app-lt" {
    name_prefix = "web_app_2"
    image_id = ""
    instance_type = "t3.micro"
    key_name = "nn.pem"

    network_interfaces {
      security_groups = [aws_security_group.app_sg.id]
      associate_public_ip_address = false
    }


  tag_specifications  {
    resource_type = "instance"
    tags = {
      Name = "launch template for app sg"
    }
  }
}

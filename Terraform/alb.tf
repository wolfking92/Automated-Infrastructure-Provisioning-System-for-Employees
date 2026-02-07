resource "aws_lb" "app_alb" {
    name = "web-app-albb"
    internal = false
    load_balancer_type = "application"

    security_groups = [aws_security_group.alb_sg.id]
    subnets = [
        aws_subnet.public_subnet_1.id,
        aws_subnet.public_subnet_2.id
    ]

    tags = {
        Name ="APPLICATION"
    }

}


resource "aws_lb_listener" "http" {
    load_balancer_arn = aws_lb.app_alb.arn
    port = 80
    protocol = "HTTP"

    default_action {
      type =  "forward"
      target_group_arn = aws_lb_target_group.app_tg.arn
    }
}

resource "aws_lb_target_group" "app_tg" {
    name = "app-tg"
    port = 5000
    protocol = "HTTP"
    target_type = "instance"
    vpc_id = aws_vpc.my_vpc_2.id

    health_check {
    path = "/"
    protocol = "HTTP"
    port = "5000"
    healthy_threshold = 2
    unhealthy_threshold = 2
    timeout = 5
    interval = 30
    }

}

resource "aws_lb_target_group_attachment" "app_ec2" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = "i-0dbd042a041e51117"
  port             = 5000
}













resource "aws_security_group" "web_sg" {
    name = "web_sg"
    vpc_id = aws_vpc.my_vpc_2.id

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks= ["0.0.0.0/0"]
    }


    egress  {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    
    tags = {
        Name = "Web_sg"
    }


}

resource "aws_security_group" "app_sg" {
    name = "app_sg"
    vpc_id = aws_vpc.my_vpc_2.id

    ingress  {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        security_groups = [aws_security_group.alb_sg.id]

    }


    egress {

        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        name = "App_sg"
    }

}

resource "aws_security_group" "alb_sg" {
    name = "alb_sg"
    vpc_id = aws_vpc.my_vpc_2.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        name = "Alb_sg"
    }



}







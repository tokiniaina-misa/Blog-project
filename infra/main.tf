provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "ci_key" {
  key_name   = var.key_pair_name
  public_key = file("ci_key.pub")
}

resource "aws_security_group" "allow_http_ssh" {
  name_prefix = "blog-sg-"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "blog" {
  ami                   = "ami-08c40ec9ead489470" # Ubuntu 22.04
  instance_type         = "t2.micro"
  key_name              = aws_key_pair.ci_key.key_name
  vpc_security_group_ids = [aws_security_group.allow_http_ssh.id]

  tags = { Name = "blog-ci" }
}

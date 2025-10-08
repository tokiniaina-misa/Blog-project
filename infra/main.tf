provider "aws" {
  region = var.aws_region
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_key_pair" "deployer" {
  key_name   = "my-key-${random_id.suffix.hex}"
  public_key = var.ssh_public_key
}

resource "aws_security_group" "docker_sg" {
  name        = "docker-sg-${random_id.suffix.hex}"
  description = "Allow SSH and HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr] # Seulement ton IP
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # HTTP public
  }
  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "docker_server" {
  ami                    = "ami-0a716d3f3b16d290c"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.docker_sg.id]

  user_data = <<-EOF
            #!/bin/bash
            set -e

            # Mise à jour et installation de Docker
            sudo apt-get update
            sudo apt-get install -y docker.io docker-compose
            sudo systemctl enable docker
            sudo systemctl start docker

            # Création du dossier pour le projet
            mkdir -p /home/ubuntu/blog-django
            chown ubuntu:ubuntu /home/ubuntu/blog-django

            # Création du fichier .env depuis la variable Terraform
            echo "${var.env_file}" > /home/ubuntu/blog-django/.env
            chmod 600 /home/ubuntu/blog-django/.env

            # Pull de la dernière image Docker
            docker pull tokiniainami/blog-django:latest

            # Supprimer le conteneur existant s’il existe
            if [ "$(docker ps -aq -f name=blog-django)" ]; then
              docker rm -f blog-django
            fi

            # Lancer le conteneur avec le .env
            docker run -d -p 8000:8000 --name blog-django \
                --env-file /home/ubuntu/blog-django/.env \
                tokiniainami/blog-django:latest

            EOF

  tags = {
    Name = "DockerServer"
  }
}

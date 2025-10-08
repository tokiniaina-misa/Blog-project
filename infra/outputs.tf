output "server_ip" {
  value       = aws_instance.docker_server.public_ip
  description = "Public IP of the Docker EC2 instance"
}

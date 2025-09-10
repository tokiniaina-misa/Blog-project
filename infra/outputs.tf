output "instance_id" {
  description = "ID de l'instance EC2 créée"
  value       = aws_instance.example.id
}

output "public_ip" {
  description = "Adresse IP publique de l'instance EC2"
  value       = aws_instance.example.public_ip
}

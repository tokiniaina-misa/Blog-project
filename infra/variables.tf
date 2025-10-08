variable "aws_region" {
  type    = string
  default = "eu-north-1"
}

variable "ssh_public_key" {
  description = "Clé publique SSH"
  type        = string
}

variable "my_ip_cidr" {
  description = "Ton IP publique avec /32 pour SSH"
  type        = string
  default     = "102.16.3.0/24"
}

variable "env_file" {
  description = "Contenu du .env à injecter"
  type        = string
  sensitive   = true
}
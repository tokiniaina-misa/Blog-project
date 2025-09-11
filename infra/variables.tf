variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "key_pair_name" {
  type = string
}

variable "allowed_ssh_cidr" {
  type = string
}

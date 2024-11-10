output "appPublicIP" {
  value = aws_instance.website.public_ip
}
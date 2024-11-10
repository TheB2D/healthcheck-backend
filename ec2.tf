resource "aws_key_pair" "my_key_pair" {
  key_name   = "my-ec2-keypair"
  public_key = file("my-ec2-keypair.pub")  # Path to your public key file
}

resource "aws_instance" "website" {
  ami           = "ami-00149760ce42c967b"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.my_key_pair.key_name  # Reference your key pair here

  user_data = <<-EOF
  #!/bin/bash
  sudo apt-get update
  sudo apt install docker.io -y
  sudo apt install python3-pip -y
  git clone https://github.com/TheB2D/healthcheck_backend.git
  sudo docker build -t health-check-backend .
  sudo docker run -p 5000:5000 health-check-backend
  EOF
}

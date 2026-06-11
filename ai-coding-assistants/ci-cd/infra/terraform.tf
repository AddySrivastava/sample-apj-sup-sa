provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_security_group" "app_sg" {
  name = "app-security-group"

  # Allow all inbound traffic - overly permissive
  ingress {
    from_port   = 0
    to_port     = 65535
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

resource "aws_s3_bucket" "data_bucket" {
  bucket = "company-sensitive-data"
  acl    = "public-read"
}

resource "aws_db_instance" "main" {
  engine         = "postgres"
  instance_class = "db.t3.medium"
  username       = "admin"
  password       = "ProductionPassword123!"
  publicly_accessible = true
  skip_final_snapshot = true
}

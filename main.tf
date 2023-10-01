provider "aws" {
  region = "us-east-1"
}

variable "project" {
  description = "The name of the project"
  type        = string
  default = "algo_arena"
}

variable "frontend_deployment_method" {
  description = "Choose the deployment method for the frontend (ec2 or other)"
  type        = string
  default     = "ec2"
}

variable "frontend_bucket" {
  description = "The name of the S3 bucket for the frontend"
  type        = string
  default     = "algo-arena-frontend"
}

resource "aws_security_group" "allow_web" {
  name        = "allow_web"
  description = "Allow inbound HTTP and HTTPS traffic"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
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

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow inbound SSH traffic"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
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

resource "aws_security_group" "allow_mysql" {
  name        = "allow_mysql"
  description = "Allow inbound traffic on MySQL default port"

  ingress {
    description = "MySQL"
    from_port   = 3306
    to_port     = 3306
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

resource "aws_security_group" "allow_daphne" {
    name        = "allow_daphne"
    description = "Allow inbound traffic on Daphne default port"

    ingress {
      description = "Daphne"
      from_port   = 8000
      to_port     = 8000
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

resource "aws_db_instance" "dbserver" {
  allocated_storage    = 10
  db_name              = "${var.project}"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "${var.project}_user"
  password             = "${var.project}_password"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  vpc_security_group_ids = [
    aws_security_group.allow_mysql.id
  ]
}

resource "aws_instance" "backend" {
  ami           = "ami-010e83f579f15bba0"
  instance_type = "t2.micro"
  key_name      = "cosc349-2023"

  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id,
    aws_security_group.allow_daphne.id,
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu" 
    private_key = file("cosc349-2023.pem") 
    host        = self.public_ip  
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir ~/backend",
      "mkdir ~/database",
    ]
  }

  provisioner "file" {
    source      = "backend/" 
    destination = "/home/ubuntu/backend"
  }

  provisioner "file" {
    source      = "database/"
    destination = "/home/ubuntu/database"
  }

  provisioner "file" {
    source      = "scripts/build-backend-vm.sh"
    destination = "/tmp/build-backend-vm.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "cd ~",
      "chmod +x /tmp/build-backend-vm.sh",
      "/tmp/build-backend-vm.sh -n ${aws_db_instance.dbserver.db_name} -u ${aws_db_instance.dbserver.username} -p ${aws_db_instance.dbserver.password} -h ${aws_db_instance.dbserver.address}"
    ]
  }

  tags = {
    Name = "Backend"
  }
}

resource "aws_instance" "frontend" {
  count         = var.frontend_deployment_method == "ec2" ? 1 : 0

  ami           = "ami-010e83f579f15bba0"
  instance_type = "t2.micro"
  key_name      = "cosc349-2023"

  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id,
    aws_security_group.allow_web.id
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu" 
    private_key = file("cosc349-2023.pem") 
    host        = self.public_ip  
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir ~/frontend",
    ]
  }

  provisioner "file" {
    source      = "frontend/" 
    destination = "/home/ubuntu/frontend"
  }

  provisioner "file" {
    source      = "scripts/build-frontend-vm.sh"
    destination = "/tmp/build-frontend-vm.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "cd ~",
      "chmod +x /tmp/build-frontend-vm.sh",
      "/tmp/build-frontend-vm.sh -h ${aws_instance.backend.public_ip}"
    ]
  }

  tags = {
    Name = "Frontend"
  }
}

resource "aws_s3_bucket" "frontend_bucket" {
  bucket = var.frontend_bucket
}

resource "aws_s3_bucket_cors_configuration" "frontend_bucket" {
  bucket = aws_s3_bucket.frontend_bucket.id  
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }  
}

resource "aws_s3_bucket_acl" "frontend_bucket" {
    bucket = aws_s3_bucket.frontend_bucket.id
    acl    = "public-read"
    depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}

resource "null_resource" "local_build" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<-EOT
      cd frontend
      npm install
      rm .env
      echo 'VITE_APP_BACKEND_HOST=${aws_instance.backend.public_ip}' >> .env
      npm run build
      aws s3 sync dist/ s3://${aws_s3_bucket.frontend_bucket.bucket}/
    EOT
  }
}


output "frontend_server_ip" {
  value = var.frontend_deployment_method == "ec2" ? aws_instance.frontend[0].public_ip : aws_s3_bucket_website_configuration.frontend[0].website_endpoint
}


output "backend_server_ip" {
  value = aws_instance.backend.public_ip
}


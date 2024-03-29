provider "aws" {
  region = "us-east-1"
}

# usage: terraform apply -var 'project=algo_arena'
variable "project" {
  description = "The name of the project"
  type        = string
  default     = "algo_arena"
}

# usage: terraform apply -var 'database_only=true'
variable "database_only" {
  description = "Shut down all the uncecessary resources and only keep the database"
  type        = bool
  default     = false
}

# usage: terraform apply -var 'frontend_deployment_method=ec2'
#        terraform apply -var 'frontend_deployment_method=s3'
variable "frontend_deployment_method" {
  description = "Choose the deployment method for the frontend (ec2 or other)"
  type        = string
  default     = "ec2"
}

# usage: terraform apply -var 'frontend_bucket=algo-arena-frontend'
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
  allocated_storage    = 20
  db_name              = var.project
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  username             = "${var.project}_user"
  password             = "${var.project}_password"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  vpc_security_group_ids = [
    aws_security_group.allow_mysql.id
  ]
}

resource "aws_instance" "backend" {
  count         = var.database_only ? 0 : 1
  ami           = "ami-010e83f579f15bba0"
  instance_type = "t2.micro"
  key_name      = "algo-arena"

  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id,
    aws_security_group.allow_daphne.id,
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("algo-arena.pem")
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
  count = var.frontend_deployment_method == "ec2" && !var.database_only ? 1 : 0

  ami           = "ami-010e83f579f15bba0"
  instance_type = "t2.micro"
  key_name      = "algo-arena"

  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id,
    aws_security_group.allow_web.id
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("algo-arena.pem")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir ~/frontend",
    ]
  }

  provisioner "local-exec" {
    command = "rm -rf frontend/dist; rm -rf frontend/node_modules"
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
      "/tmp/build-frontend-vm.sh -h ${aws_instance.backend[0].public_ip}"
    ]
  }

  tags = {
    Name = "Frontend"
  }
}

resource "aws_s3_bucket" "frontend_bucket" {
  count         = var.frontend_deployment_method == "ec2" && !var.database_only ? 0 : 1
  bucket        = var.frontend_bucket
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "frontend_bucket" {
  count  = var.frontend_deployment_method == "ec2" && !var.database_only ? 0 : 1
  bucket = aws_s3_bucket.frontend_bucket[0].bucket

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


resource "null_resource" "local_build" {
  count = var.frontend_deployment_method == "ec2" && !var.database_only ? 0 : 1
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<-EOT
      cd frontend
      npm install
      rm .env
      echo 'VITE_APP_BACKEND_HOST=${aws_instance.backend[0].public_ip}' >> .env
      npm run build
      aws s3 sync dist/ s3://${aws_s3_bucket.frontend_bucket[0].bucket}/
    EOT
  }
}

# output "frontend_server_ip" {
#   value = var.frontend_deployment_method == "ec2" ? aws_instance.frontend[0].public_ip : "N/A"
# }

output "backend_server_ip" {
  value = aws_instance.backend[0].public_ip
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  count = var.frontend_deployment_method == "ec2" && !var.database_only ? 0 : 1
  depends_on = [
    null_resource.local_build,
    aws_s3_bucket.frontend_bucket,
    aws_s3_bucket_public_access_block.frontend_bucket
  ]
  bucket = aws_s3_bucket.frontend_bucket[0].bucket

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "frontend" {
  count = var.frontend_deployment_method == "ec2" && !var.database_only ? 0 : 1
  depends_on = [
    null_resource.local_build,
    aws_s3_bucket.frontend_bucket,
    aws_s3_bucket_public_access_block.frontend_bucket
  ]
  bucket = aws_s3_bucket.frontend_bucket[0].bucket
  policy = <<POLICY
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
            "s3:GetObject"
          ],
          "Resource": [
            "arn:aws:s3:::${aws_s3_bucket.frontend_bucket[0].bucket}/*"
          ]
        }
      ]
    }
  POLICY
}

output "frontend_url" {
  value = var.frontend_deployment_method == "ec2" ? "http://${aws_instance.frontend[0].public_ip}" : "http://${aws_s3_bucket.frontend_bucket[0].bucket}.s3-website-us-east-1.amazonaws.com"
}

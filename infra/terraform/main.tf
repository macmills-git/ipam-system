terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
resource "aws_vpc" "ipam_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ipam-vpc"
  }
}

resource "aws_subnet" "ipam_subnet_a" {
  vpc_id            = aws_vpc.ipam_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "ipam-subnet-a"
  }
}

resource "aws_subnet" "ipam_subnet_b" {
  vpc_id            = aws_vpc.ipam_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "ipam-subnet-b"
  }
}

resource "aws_internet_gateway" "ipam_igw" {
  vpc_id = aws_vpc.ipam_vpc.id

  tags = {
    Name = "ipam-igw"
  }
}

resource "aws_route_table" "ipam_rt" {
  vpc_id = aws_vpc.ipam_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ipam_igw.id
  }

  tags = {
    Name = "ipam-rt"
  }
}

resource "aws_route_table_association" "ipam_rta_a" {
  subnet_id      = aws_subnet.ipam_subnet_a.id
  route_table_id = aws_route_table.ipam_rt.id
}

resource "aws_route_table_association" "ipam_rta_b" {
  subnet_id      = aws_subnet.ipam_subnet_b.id
  route_table_id = aws_route_table.ipam_rt.id
}

# Security Groups
resource "aws_security_group" "ipam_alb_sg" {
  name        = "ipam-alb-sg"
  description = "Security group for IPAM ALB"
  vpc_id      = aws_vpc.ipam_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
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

  tags = {
    Name = "ipam-alb-sg"
  }
}

resource "aws_security_group" "ipam_app_sg" {
  name        = "ipam-app-sg"
  description = "Security group for IPAM application"
  vpc_id      = aws_vpc.ipam_vpc.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.ipam_alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ipam-app-sg"
  }
}

resource "aws_security_group" "ipam_db_sg" {
  name        = "ipam-db-sg"
  description = "Security group for IPAM database"
  vpc_id      = aws_vpc.ipam_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ipam_app_sg.id]
  }

  tags = {
    Name = "ipam-db-sg"
  }
}

# RDS PostgreSQL
resource "aws_db_subnet_group" "ipam_db_subnet_group" {
  name       = "ipam-db-subnet-group"
  subnet_ids = [aws_subnet.ipam_subnet_a.id, aws_subnet.ipam_subnet_b.id]

  tags = {
    Name = "ipam-db-subnet-group"
  }
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "ipam_db_password" {
  name = "ipam-db-password-${random_id.suffix.hex}"
}

resource "aws_secretsmanager_secret_version" "ipam_db_password" {
  secret_id     = aws_secretsmanager_secret.ipam_db_password.id
  secret_string = random_password.db_password.result
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_db_instance" "ipam_db" {
  identifier             = "ipam-db"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  storage_type           = "gp3"
  db_name                = "ipam"
  username               = "ipam"
  password               = random_password.db_password.result
  db_subnet_group_name   = aws_db_subnet_group.ipam_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.ipam_db_sg.id]
  skip_final_snapshot    = var.environment == "dev"
  backup_retention_period = 7
  multi_az               = var.environment == "prod"

  tags = {
    Name = "ipam-db"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "ipam_cluster" {
  name = "ipam-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "ipam-cluster"
  }
}

# ECR Repositories
resource "aws_ecr_repository" "ipam_backend" {
  name                 = "ipam-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "ipam_frontend" {
  name                 = "ipam-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Application Load Balancer
resource "aws_lb" "ipam_alb" {
  name               = "ipam-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ipam_alb_sg.id]
  subnets            = [aws_subnet.ipam_subnet_a.id, aws_subnet.ipam_subnet_b.id]

  tags = {
    Name = "ipam-alb"
  }
}

resource "aws_lb_target_group" "ipam_backend_tg" {
  name        = "ipam-backend-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.ipam_vpc.id
  target_type = "ip"

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 60
    interval            = 300
    matcher             = "200"
  }
}

resource "aws_lb_listener" "ipam_http" {
  load_balancer_arn = aws_lb.ipam_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ipam_backend_tg.arn
  }
}

# Outputs
output "db_endpoint" {
  value       = aws_db_instance.ipam_db.endpoint
  description = "RDS database endpoint"
}

output "alb_dns_name" {
  value       = aws_lb.ipam_alb.dns_name
  description = "Application Load Balancer DNS name"
}

output "ecr_backend_url" {
  value       = aws_ecr_repository.ipam_backend.repository_url
  description = "ECR repository URL for backend"
}

output "ecr_frontend_url" {
  value       = aws_ecr_repository.ipam_frontend.repository_url
  description = "ECR repository URL for frontend"
}

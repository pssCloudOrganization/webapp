packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8, < 2.0.0"
      source  = "github.com/hashicorp/amazon"
    }
    googlecompute = {
      version = ">= 1.0.0, < 2.0.0"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

variable "aws_ami_name" {
  type    = string
  default = env("AWS_AMI_NAME")
}

variable "aws_instance_type" {
  type    = string
  default = env("AWS_INSTANCE_TYPE")
}

variable "aws_region" {
  type    = string
  default = env("AWS_REGION")
}

variable "aws_ssh_username" {
  type    = string
  default = env("AWS_SSH_USERNAME")
}

variable "aws_subnet_id" {
  type    = string
  default = env("AWS_SUBNET_ID")
}

variable "aws_vpc_id" {
  type    = string
  default = env("AWS_VPC_ID")
}

variable "aws_dev_user" {
  type    = string
  default = env("AWS_DEV_USER")
}

variable "aws_demo_user" {
  type    = string
  default = env("AWS_DEMO_USER")
}

variable "aws_source_ami" {
  type    = string
  default = env("AWS_SOURCE_AMI")
}

variable "aws_access_key" {
  type    = string
  default = env("GA_AWS_ACCESS_KEY")
}

variable "aws_secret_key" {
  type    = string
  default = env("GA_AWS_SECRET_ACCESS_KEY")
}

variable "DEFAULT_USER" {
  type    = string
  default = env("DEFAULT_USER")
}

variable "DEFAULT_PASS" {
  type    = string
  default = env("DEFAULT_PASS")
}

variable "MYSQL_USER" {
  type    = string
  default = env("MYSQL_USER")
}

variable "MYSQL_PASSWORD" {
  type    = string
  default = env("MYSQL_PASSWORD")
}

variable "HOST" {
  type    = string
  default = env("HOST")
}

variable "DB_NAME" {
  type    = string
  default = env("DB_NAME")
}

variable "gcp_project_id" {
  type    = string
  default = env("GCP_PROJECT_ID")
}

variable "gcp_source_image" {
  type    = string
  default = env("GCP_SOURCE_IMAGE")
}

variable "gcp_ssh_username" {
  type    = string
  default = env("GCP_SSH_USERNAME")
}

variable "gcp_zone" {
  type    = string
  default = env("GCP_ZONE")
}

variable "gcp_disk_size" {
  type    = string
  default = env("GCP_DISK_SIZE")
}

variable "gcp_machine_type" {
  type    = string
  default = env("GCP_MACHINE_TYPE")
}


source "amazon-ebs" "ubuntu" {
  ami_name        = "csye6225_${var.aws_ami_name}_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI webapp aws"
  source_ami      = var.aws_source_ami
  instance_type   = var.aws_instance_type
  region          = var.aws_region
  ssh_username    = var.aws_ssh_username
  subnet_id       = var.aws_subnet_id
  vpc_id          = var.aws_vpc_id
  ami_users       = [var.aws_dev_user, var.aws_demo_user]

  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
    delete_on_termination = true
  }
}

source "googlecompute" "ubuntu" {
  image_name        = "csye6225-${var.aws_ami_name}-${formatdate("YYYY-MM-DD-hh-mm-ss", timestamp())}"
  image_description = "Machine Image GCP"
  project_id        = var.gcp_project_id
  source_image      = var.gcp_source_image
  ssh_username      = var.gcp_ssh_username
  zone              = var.gcp_zone
  disk_size         = var.gcp_disk_size
  machine_type      = var.gcp_machine_type
}


build {
  name = "assignment-4"
  sources = [
    "source.amazon-ebs.ubuntu",
    "source.googlecompute.ubuntu",
  ]

  provisioner "file" {
    source      = "./.env"
    destination = "/tmp/"
  }

  provisioner "file" {
    source      = "webapp.zip"
    destination = "/tmp/"
  }
  provisioner "file" {
    source      = "csye6225.service"
    destination = "/tmp/"
  }

  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1",
      "DEFAULT_USER=${var.DEFAULT_USER}",
      "DEFAULT_PASS=${var.DEFAULT_PASS}",
      "MYSQL_USER=${var.MYSQL_USER}",
      "MYSQL_PASSWORD=${var.MYSQL_PASSWORD}",
      "HOST=${var.HOST}",
      "DB_NAME=${var.DB_NAME}"
    ]
    inline = [
      "sleep 10",
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt install -y unzip python3-pip pkg-config python3-venv default-libmysqlclient-dev mysql-server",
      # "sudo apt install -y unzip python3-pip pkg-config libmysqlclient-dev mysql-server",
      # "sudo apt-get install -y unzip python3-pip python3-venv libmysqlclient-dev mysql-server",
      "sudo systemctl enable mysql",
      "sudo systemctl start mysql",
      "sudo mysql -u $DEFAULT_USER -p$DEFAULT_PASS -e\"CREATE USER '$MYSQL_USER'@'$HOST' IDENTIFIED BY '$MYSQL_PASSWORD';\"",
      "sudo mysql -u $DEFAULT_USER -p$DEFAULT_PASS -e\"CREATE DATABASE $DB_NAME;\"",
      "sudo mysql -u $DEFAULT_USER -p$DEFAULT_PASS -e\"GRANT ALL PRIVILEGES ON test_$DB_NAME.* TO '$MYSQL_USER'@'$HOST' WITH GRANT OPTION;\"",
      "sudo mysql -u $DEFAULT_USER -p$DEFAULT_PASS -e\"GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$MYSQL_USER'@'$HOST' WITH GRANT OPTION;\"",
      "sudo mysql -u $DEFAULT_USER -p$DEFAULT_PASS -e\"FLUSH PRIVILEGES;\""
    ]
  }

  provisioner "shell" {
    script = "app-init.sh"
  }
}



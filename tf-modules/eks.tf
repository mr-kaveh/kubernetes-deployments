provider "aws" {
  region = "us-west-2"  # Change to your desired AWS region
}

provider "kubernetes" {
  config_path = "~/.kube/config"  # Change to the path of your kubeconfig file
}

resource "aws_eks_cluster" "my_cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = ["subnet-abcde012", "subnet-bcde012a", "subnet-cde012ab"]  # Change to your VPC subnet IDs
    security_group_ids = ["sg-0123456789abcdef"]  # Change to your security group IDs
  }
}

resource "aws_eks_node_group" "my_node_group" {
  cluster_name    = aws_eks_cluster.my_cluster.name
  node_group_name = "my-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn

  scaling_config {
    desired_size = 2
    max_size     = 2
    min_size     = 1
  }

  remote_access {
    ec2_ssh_key = "my-ssh-key"
    source_security_group_ids = ["sg-0123456789abcdef"]  # Change to your security group IDs
  }

  subnet_ids = ["subnet-abcde012", "subnet-bcde012a", "subnet-cde012ab"]  # Change to your VPC subnet IDs
}

resource "aws_iam_role" "eks_cluster_role" {
  name               = "eks-cluster-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role" "eks_node_role" {
  name               = "eks-node-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

output "kubeconfig" {
  value = aws_eks_cluster.my_cluster.kubeconfig
}

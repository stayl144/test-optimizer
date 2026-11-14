terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    # CHANGE ACCOUNT_ID to your 12-digit AWS account number
    bucket         = "cro-tfstate-882224612683"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cro-tflock"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      app                 = "crew-reserve-optimizer"
      env                 = terraform.workspace
      data_classification = "confidential"
      owner               = "platform-team"
    }
  }
}

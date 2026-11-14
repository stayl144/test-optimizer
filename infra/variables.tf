variable "image_uri" {
  description = "ECR image by digest, e.g. ...crew-reserve-optimizer@sha256:abc"
  type        = string
}

variable "alert_email" { type = string }

locals {
  env  = terraform.workspace
  name = "cro-${terraform.workspace}"
}

data "aws_caller_identity" "me" {}

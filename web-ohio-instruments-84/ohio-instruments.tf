locals {
  flag = "bctf{n07_4ppr0v3d_by_7h3_c0ll3g3_b04rd_d210c7c6}"
}

module "ohio-instruments-84" {
  source            = "../../../challenge"
  challenge_cluster = var.challenge_cluster
  stages            = var.stages
  stage             = "stage1"
  name              = "Ohio Instruments 84"
  description       = "Locally sourced graphing calculator.\n\n[https://ohio-instruments-84.chall.pwnoh.io](https://ohio-instruments-84.chall.pwnoh.io)"
  category          = "web"
  author            = "jm8"
  difficulty        = "medium"
  flag              = local.flag
  identifier        = "web-ohio-instruments-84"

  memory            = 512

  port_mappings = [
    {
      local_port     = 1024
      http_subdomain = "ohio-instruments-84"
      global_index   = var.initial_index
    }
  ]

  files = [{
    name = "export.zip",
    url  = "https://buckeyectf23-stage1.s3.us-east-2.amazonaws.com/web-ohio-instruments-84/export.zip"
  }]
}

variable "initial_index" {
  type = number
}

variable "challenge_cluster" {}
variable "stages" {}

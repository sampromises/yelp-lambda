# Variables
provider "aws" {
  region = "us-east-1"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}


# Lambda
resource "aws_lambda_function" "dispatcher_lambda" {
  filename = "lambda.zip"
  function_name = "yelp_dispatcher_lambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "lambda.dispatcher_handler"
  runtime = "python3.8"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda.zip"))}"
  source_code_hash = "${filebase64sha256("lambda.zip")}"
}

resource "aws_lambda_function" "worker_lambda" {
  filename = "lambda.zip"
  function_name = "yelp_worker_lambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "lambda.worker_handler"
  runtime = "python3.8"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda.zip"))}"
  source_code_hash = "${filebase64sha256("lambda.zip")}"
}

# IAM
resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

resource "aws_iam_policy_attachment" "attach-AWSLambdaBasicExecutionRole" {
  name = "attach-AWSLambdaBasicExecutionRole"
  roles = [
    "${aws_iam_role.lambda_role.name}"
  ]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy_attachment" "attach-AWSLambdaRole" {
  name = "attach-AWSLambdaRole"
  roles = [
    "${aws_iam_role.lambda_role.name}"
  ]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
}

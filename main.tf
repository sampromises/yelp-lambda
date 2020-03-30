# Variables
provider "aws" {
  region = "us-east-1"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}


# Lambda
resource "aws_lambda_function" "dispatcher_lambda" {
  filename = "lambda.zip"
  function_name = "YelpDispatcherLambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "lambda.dispatcher_handler"
  runtime = "python3.8"
  memory_size = "128"
  timeout = 60

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda.zip"))}"
  source_code_hash = "${filebase64sha256("lambda.zip")}"
}

resource "aws_lambda_function" "worker_lambda" {
  filename = "lambda.zip"
  function_name = "YelpWorkerLambda"
  role = "${aws_iam_role.lambda_role.arn}"
  handler = "lambda.worker_handler"
  runtime = "python3.8"
  memory_size = "128"
  timeout = 60

  environment {
    variables = {
      RESULTS_QUEUE_NAME = "${aws_sqs_queue.yelp-results-queue.name}"
    }
  }

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

resource "aws_iam_policy" "allow-yelp-results-queue-access" {
  name        = "allow-yelp-results-queue-access"
  description = "Allow Lambda to send message to yelp-results-queue SQS queue"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage",
        "sqs:GetQueueUrl"
      ],
      "Resource": [
        "${aws_sqs_queue.yelp-results-queue.arn}"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "attach-allow-yelp-results-queue-access" {
  name = "attach-AWSLambdaRole"
  roles = [
    "${aws_iam_role.lambda_role.name}"
  ]
  policy_arn = "${aws_iam_policy.allow-yelp-results-queue-access.arn}"
}

# SQS
resource "aws_sqs_queue" "yelp-results-queue" {
  name = "YelpResultsQueue"
  message_retention_seconds = 1209600
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.yelp-results-dlq.arn
    maxReceiveCount = 4
  })
}

resource "aws_sqs_queue" "yelp-results-dlq" {
  name = "YelpResultsDLQ"
  message_retention_seconds = 1209600
}

resource "aws_sqs_queue_policy" "test" {
  queue_url = "${aws_sqs_queue.yelp-results-queue.id}"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.yelp-results-queue.arn}"
    }
  ]
}
POLICY
}

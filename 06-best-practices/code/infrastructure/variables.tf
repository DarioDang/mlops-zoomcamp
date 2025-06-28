variable "aws_region" {
    description = "AWS region to deploy resources"
    default     = "ap-southeast-2"
}

variable "project_id" {
    description = "project_id"
    default = "mlops-zoomcamp"
}

variable "source_stream_name" {
    description = "Source Kinesis Data Stream name"
}

variable "output_stream_name" {
    description = "Output Kinesis Data Stream name"
}

variable "model_bucket" {
    description = "The name of the S3 bucket to create."
}

variable "lambda_function_local_path" {
  description = ""
}

variable "docker_image_local_path" {
  description = ""
}

variable "ecr_repo_name" {
  description = ""
}

variable "lambda_function_name" {
  description = ""
}

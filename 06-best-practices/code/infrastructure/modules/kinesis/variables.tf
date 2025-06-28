variable "stream_name" {
  description = "The name of the Kinesis Data Stream"
  type        = string
}

variable "shard_count" {
  description = "The number of shards for the Kinesis Data Stream"
  type        = number
}

variable "retention_period" {
  description = "The retention period (in hours) for the Kinesis Data Stream"
  type        = number
}

variable "shard_level_metrics" {
  description = "A list of shard-level metrics to enable for the Kinesis Data Stream"
  type        = list(string)
  default     = [
    "IncomingBytes",
    "OutgoingBytes",
    "OutgoingRecords",
    "ReadProvisionedThroughputExceeded",
    "WriteProvisionedThroughputExceeded",
    "IncomingRecords",
    "IteratorAgeMilliseconds",
  ]
}

variable "tags" {
  description = "Tags to assign to the Kinesis Data Stream"
  default     = "mlops-zoomcamp"
}
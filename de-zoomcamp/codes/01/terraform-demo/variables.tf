variable "credentials" {
  description = "My Credentials"
  default     = "./keys/creds.json"
}

variable "project" {
  description = "Project"
  default     = "civic-radio-485413-b3"
}

variable "region" {
  description = "Region"
  default     = "asia-southeast1"
}

variable "location" {
  description = "Project Location"
  default     = "ASIA-SOUTHEAST1"
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket name"
  default     = "civic-radio-485413-b3-terraform-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

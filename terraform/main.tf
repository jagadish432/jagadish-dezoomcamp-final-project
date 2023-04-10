terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${var.project_name}"
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

resource "google_storage_bucket_object" "pyspark_file" {
  name   = "generate_stats_dataproc.py"
  source = "../pyspark_jobs/generate_stats_dataproc.py"
  bucket = google_storage_bucket.data-lake-bucket.name
}

# # not used for now, but this can be sued for auto triggering the dataproc job
# resource "google_storage_bucket_object" "python_trigger_dataproc" {
#   name   = "submit_dataproc_job.py"
#   bucket = google_storage_bucket.data-lake-bucket.name
#   source = "../pyspark_jobs/submit_dataproc_job.py"
# }

# DataWare House
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = replace(var.project_name, "-", "_")
  project    = var.project_id
  location   = var.region
}

# Artifact repository for docker images
resource "google_artifact_registry_repository" "ipl-project" {
  location = var.region
  repository_id = var.project_name
  description = "Jagadeesh Dachepalli's IPL project google artifact repository"
  format = "DOCKER"
}
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
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
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

resource "google_storage_bucket_object" "python_trigger_dataproc" {
  name   = "submit_dataproc_job.py"
  bucket = google_storage_bucket.data-lake-bucket.name
  source = "../pyspark_jobs/submit_dataproc_job.py"
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}


resource "google_artifact_registry_repository" "ipl-project" {
  location = var.region
  repository_id = "ipl-project"
  description = "Jagadeesh Dachepalli's IPL project google artifact repository"
  format = "DOCKER"
}
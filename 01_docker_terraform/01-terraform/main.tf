terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.22.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = file(var.credentials) # use file() open the dir
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name # Globally unique
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1 # in days
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
# resource "google_service_account" "default" {
#   account_id   = "service-account-id"
#   display_name = var.DATAPROC_CLSUTER
# }

resource "google_dataproc_cluster" "mycluster" {
  name     = var.DATAPROC_CLSUTER
  region   = var.region
  graceful_decommission_timeout = "120s"
  labels = {
    owner = "jagadish"
  }

  cluster_config {
    staging_bucket = google_storage_bucket.data-lake-bucket.name
    # Override or set some custom properties
    software_config {
      image_version = "2.0.35-debian10"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
    }

    master_config {
      num_instances = 1
      machine_type  = "e2-medium"
      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 30
      }
    }

    worker_config {
      num_instances    = 2
      machine_type     = "e2-medium"
      disk_config {
        boot_disk_size_gb = 30
      }
    }

    preemptible_worker_config {
      num_instances = 0
    }
  }
  
}

# Submit an example pyspark job to a dataproc cluster
resource "google_dataproc_job" "pyspark" {
  region       = google_dataproc_cluster.mycluster.region
  force_delete = true
  placement {
    cluster_name = google_dataproc_cluster.mycluster.name
  }

  pyspark_config {
    main_python_file_uri = "gs://${google_storage_bucket.data-lake-bucket.name}/${google_storage_bucket_object.pyspark_file.name}"
    jar_file_uris=["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"]
    properties = {
      "spark.logConf" = "true"
    }
  }
}
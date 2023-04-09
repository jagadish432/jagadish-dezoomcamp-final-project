output gcp_bucket_name {
    value=google_storage_bucket.data-lake-bucket.name
}

output gcp_bigquery_dataset_name{
    value=google_bigquery_dataset.dataset.dataset_id
}

output gcp_artifact_repository {
    value=google_artifact_registry_repository.ipl-project.id
}

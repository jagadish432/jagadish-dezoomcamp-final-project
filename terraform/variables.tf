variable "project_name" {
  description = "name of the project, we use this for all of our gcp resources names"
  type = string
}

variable "project_id" {
  description = "Your GCP Project ID"
  type = string 
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

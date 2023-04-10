## Terraform deployment.
A. Change to `terraform` directory - i.e., run `cd terraform/` 
B. Before deploying, please 'Enable' these APIs - billing, artifact, dataproc, cloud run in the gcp console

1. Run `terraform init` to download required terraform packages.
2. Run `terraform apply -var 'project=<project-id-from-gcp>`- to apply the changes, we need to replace the project id, in this command. This may take 5-10 minutes as it need to create some resources in gcp cloud and along with a dataproc cluster resource.
3. Run `terraform output` to check (or) display the output values

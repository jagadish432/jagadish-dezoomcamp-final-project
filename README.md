# jagadish-dezoomcamp-final-project
This is Final project by Jagadeesh Dachepalli as part of DataTalksClub DE Zoomcamp 

## Need to run the below steps in the mentioned order to be able create all this project required resources in GCP cloud and test this project

### Pre-requisites
1. make sure you have a gcp service account, go to `https://console.cloud.google.com/iam-admin/serviceaccounts?project=<gcp-project-name>` in this case `https://console.cloud.google.com/iam-admin/serviceaccounts?project=datazoomcamp-jagadish-final` 
2. select the service account and select `manage keys`
3. select `Add key` and `JSON` and save the automatically downloaded .json file somewhere in a safe location
4. `gcloud auth login`, click on the link, allow access, copy the code and paste in the terminal prompting for the authorization code
5. verify if the project is already set with your required project `gcloud config get project`
6. if not, then `gcloud config set project <gcp-project-name>`
7. To set the gcloud automatically access the required project, follow either of the below approaches
    a. REFRESH TOKEN approach
        1. run `gcloud auth application-default login` and enter Y when prompted, click on the link provided and login to the gcp console and copy the authorization code and paste in the terminal where prompted
        2. verify `~/.config/gcloud/application_default_credentials.json` it has the updated and the required project creds now
        3. `unset GOOGLE_APPLICATION_CREDENTIALS`

### Terraform
1. `terraform init`
2. `terraform apply`
3. `terraform output` to validate the output values

### Prefect
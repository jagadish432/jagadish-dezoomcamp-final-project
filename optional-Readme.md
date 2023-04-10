4. Run `gcloud auth activate-service-account --key-file <path to the json file of the service account we want to use>`
5. Verify if service account has been added or not by `gcloud config list`
6. verify if the project is already set with your required project `gcloud config get project`
7. if not, then `gcloud config set project <gcp-project-id-from-gcp>`
8. run `gcloud auth application-default login`

FYI(Optional)
9. To set the gcloud automatically access the required project, follow either of the below approaches
    a. REFRESH TOKEN approach
        1. run `gcloud auth application-default login` and enter Y when prompted, click on the link provided and login to the gcp console and copy the authorization code and paste in the terminal where prompted
        2. verify `~/.config/gcloud/application_default_credentials.json` it has the updated and the required project creds now
        3. `unset GOOGLE_APPLICATION_CREDENTIALS`
    b. To use the download gcp creds file directly(json file)
        1. cd to `~/.gc/`
        2. create a json file and copy the content
        3. now set the env variable `export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/<json file_name>`
        4. keep the above export command in your bash profile file to make it permanent env variable i.e., you wouldn't need to set everytime you open a terminal
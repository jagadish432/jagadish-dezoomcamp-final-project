## VM machine setup
0. All GCP compute instances by default comes with `gcloud` SDK in-built, if you're using any other VM or your own computer then please install the gcloud cli SDK.
1. Add `alias python=python3` in bashrc file to make python default version to python3's version
2. Run `sudo apt-get update` to update the packages (in case of ubuntu/linux machines)
3. Run `sudo apt-get install docker.io` to install docker
4. To make docker work without sudo, run the below commands:
    a. `sudo groupadd docker`
    b. `sudo gpasswd -a $USER docker`
    c. `sudo service docker restart`
5. Run `sudo apt-get install unzip` to install 'unzip', and do the same for 'wget' as well which we use to download any files.
6. Copy terraform binary(get the URL from terraform website homepage) inside `~/bin` folder(create if bin doesn't exist), unzip and remove the zip file.
7. Add `export PATH="${HOME}/bin:${PATH}"` at end of ~/.bashrc file to make terraform visible to the system variables.

## VM machine - to connect to GCP account
0. Have a GCP account and create a project in GCP console
1. Go to `Service Accounts` in the GCP Console, Select the service account and select `manage keys` and Add a key to the service account and and save the automatically downloaded .json file somewhere in a safe location
3. Have the gcloud cli on the system you're planning to test this, store the above json key file in `~/.gc/` (create if .gc folder doesn't exist)
4. Add `export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/creds.json` in the bashrc file
5. Run `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` to link a service account on the VM/system we're working on.
6. Provide the gcp project id to the variabele `gcp_project_id` in this [var file](./config/vars) 
7. Provide the GCP project ID and porject Name to the 'project_id' and 'project_name' variables in the [pyspark file](./pyspark_jobs/generate_stats_dataproc.py) respectively.
8. Now, run `source config/vars`
# anthos-edge-management
Google Cloud Edge Device Management

## Run Code Locally
```
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r src/requirements.txt
export GCP_PROJECT=$(gcloud config get-value project)
export SOURCE_REPO="https://github.com/greavr/anthos-edge-acm"
export VM_IMAGE_BUCKET="https://storage.googleapis.com/rgreaves-gke-chaos-kubevirt"
python3 src/main.py
```
Then you can browse the code [localhost:8080](http://localhost:8080).<br /><br />

### Documentation ###
You can also view the documentation locally on [localhost:8080/docs](http://localhost:8080)


**Deactivate the environment** 
Run the following command
```
deactivate
```


## Environment Variables ##
The following environment variables can be set:
  - **GCP_PROJECT** - Name of the target GCP
  - **SOURCE_REPO** - URL to the REPO for ACM Git
  - **GIT_TOKEN** - Git Hub Token [Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
  - **COPY_FROM_REPO** - Source repo with sample workloasd [github.com/greavr/anthos-edge-workloads](https://github.com/greavr/anthos-edge-workloads)
  - **SAVE_PATH** - Local save path (has a default value)
  - **VM_IMAGE_BUCKET** - GCS Bucket which holds the KubeVirt VM Images

# Org Policy:
- **iam.allowedPolicyMemberDomains** - Set To ***All***
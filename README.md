# anthos-edge-management - offline Demo Branch
Google Cloud Edge Device Management

## Run Code Locally
```
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r src/requirements.txt
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
  - **SOURCE_REPO** - URL to the REPO for ACM Git
  - **LATENCY_GRAPH_URL** - URL for the specific latency graph to display in iframe on syncronicity page
  - **SYNC_LOOKER_URL** - URL for the Looker dashboard in the syncronicity page
  - **GRAFANA_URL** - OPTIONAL URL for Grafana Service
  - **POS_URL** - URL For the POS System used

# Org Policy:
- **iam.allowedPolicyMemberDomains** - Set to***All***
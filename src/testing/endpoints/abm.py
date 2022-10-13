from datetime import datetime
import random
from fastapi import APIRouter
from typing import List

from core.helper import helper

from models.abm import Abm
from models.logs import abm_log_item
from models.urls import abm_url_list
from models.abm_node import AbmNode

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/testing/abm",
    tags=["testing"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Abm])
async def list_of_abm_clusters():
    """ Function returns list of Anthos Baremetal Clusters in the project: TESTING - ALWAYS SUCCESS """  
    canned_values = []
    gcp_regions = ["asia-east1","asia-east2","asia-northeast1","asia-northeast2","asia-northeast3","asia-south1","asia-south2","asia-southeast1","asia-southeast2","australia-southeast1","australia-southeast2","europeentral2","europe-north1","europe-southwest1","europe-west1-d","europe-west2","europe-west3","europe-west4","europe-west6","europe-west8","europe-west9","northamerica-northeast1","northamerica-northeast2","southamerica-east1","southamerica-west1","usentral1","us-east1-d","us-east4","us-east5","us-south1","us-west1","us-west2","us-west3","us-west4"]

    for a_region in gcp_regions:
        nodes = random.randint(2, 9)
        this_abm = Abm(
            name=f"abm-{a_region}",
            location=a_region,
            version="v1.22.8-gke.200",
            node_count=nodes,
            vcpu_count=nodes*4,
            memory_mb=(nodes*1024)*4,
            cluster_state="READY",
            update_time=datetime.now(),
            acm_status="Ready",
            acm_update_time=datetime.now(),
            lat_long = helper.lookup_location(gcp_region=a_region),
            labels={
                "canary" : random.choice(["100","50","25","10"]),
                "continent" : a_region.split("-")[0],
                "loc" : a_region
            }
        )
        canned_values.append(this_abm)
    
    return canned_values

@router.get("/logs/", response_model=List[abm_log_item])
async def cluster_details(cluster_name: str, row_count: int = 100):
    """ Get a list of logs from the ABM Cluster : TESTING - ALWAYS SUCCESS"""  
    canned_values = []

    for log_num in range(100):
        a_log = abm_log_item(
            severity=random.choice(["DEFAULT","ERROR","INFO"]),
            timestamp=datetime.now(),
            data="ProtobufEntry(log_name='projects/anthos-edge-361104/logs/externalaudit.googleapis.com%2Factivity', labels={'authorization.k8s.io/decision': 'allow', 'authorization.k8s.io/reason': 'RBAC: allowed by RoleBinding \"canonical-service-leader-election-rolebinding/asm-system\" of Role \"canonical-service-leader-election-role\" to ServiceAccount \"canonical-service-account/asm-system\"'}, insert_id='52539a60-e14f-46dd-803b-c70426afe2a1', severity=None, http_request=None, timestamp=datetime.datetime(2022, 9, 25, 21, 51, 42, 411862, tzinfo=datetime.timezone.utc), resource=Resource(type='k8s_cluster', labels={'cluster_name': 'abm-northamerica-northeast1', 'location': 'northamerica-northeast1', 'project_id': 'anthos-edge-361104'}), trace=None, span_id=None, trace_sampled=None, source_location=None, operation={'id': '52539a60-e14f-46dd-803b-c70426afe2a1', 'producer': 'anthosgke.googleapis.com', 'first': True, 'last': True}, logger=<google.cloud.logging_v2.logger.Logger object at 0x3e606b4bbb20>, payload=OrderedDict([('@type', 'type.googleapis.com/google.cloud.audit.AuditLog'), ('status', {}), ('authenticationInfo', {'principalEmail': 'system:serviceaccount:asm-system:canonical-service-account'}), ('requestMetadata', {'callerIp': '10.200.0.5', 'callerSuppliedUserAgent': 'manager/v0.0.0 (linux/amd64) kubernetes/$Format'}), ('serviceName', 'anthosgke.googleapis.com'), ('methodName', 'io.k8s.core.v1.configmaps.update'), ('authorizationInfo', [{'resource': 'core/v1/namespaces/asm-system/configmaps/8f5e826b.cloud.google.com', 'permission': 'io.k8s.core.v1.configmaps.update', 'granted': True}]), ('resourceName', 'core/v1/namespaces/asm-system/configmaps/8f5e826b.cloud.google.com')]))"
        )
        canned_values.append(a_log)
    
    return canned_values

@router.get("/urls/", response_model=abm_url_list)
async def testing_cluster_details(cluster_name: str):
    canned_urls = abm_url_list(
        store_pages=["http://104.198.3.165/","http://34.168.57.77/restaurant"],
        monitoring_dashboar="http://34.82.239.219:3000/",
        metrics_endpoint = "http://35.193.141.59:8080/"  )
    return canned_urls

@router.get("/nodes/", response_model=List[AbmNode])
async def node_list(cluster_name: str, location:str):
    """ Return details of nodes in the cluster : TESTING - ALWAYS SUCCESS"""  
    canned_values = [
        {"name": "abm-master-northamerica-northeast1-0","zone": "northamerica-northeast1-a","ip": "10.0.8.9","instance_type": "n2-standard-2","disk_size_gb": 160,"update_time": "2022-09-26T21:45:51.101184", "status": "RUNNING"},
        {"name": "abm-worker-northamerica-northeast1-0","zone": "northamerica-northeast1-a","ip": "10.0.8.11","instance_type": "n2-standard-2","disk_size_gb": 160,"update_time": "2022-09-26T21:45:51.101379", "status": "STOPPED"},
        {"name": "abm-worker-northamerica-northeast1-1","zone": "northamerica-northeast1-a","ip": "10.0.8.10","instance_type": "n2-standard-2","disk_size_gb": 160,"update_time": "2022-09-26T21:45:51.101453", "status": "RUNNING"}
    ]
    return canned_values

@router.post("/set-urls/", responses={
    200: {
        "description": "Update Cluster URLS",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to Update Cluster URLS"}
})
async def save_abm_urls(cluster_name: str, url_list: abm_url_list):
    """ Update Cluster URLS : TESTING - ALWAYS SUCCESS"""
    return {"status":"success"}

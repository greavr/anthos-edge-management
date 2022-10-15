from fastapi import APIRouter, HTTPException
from typing import List
import json

from core.gcp import gcp, logging, gce
from models.abm import Abm
from models.logs import abm_log_item
from models.urls import abm_url_list
from models.abm_node import AbmNode
from models.vm import vm_info


#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/v1/abm",
    tags=["abm"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Abm])
async def list_of_abm_clusters():
    """ Function returns list of Anthos Baremetal Clusters in the project"""
    return gcp.get_abm_list()

@router.get("/logs/", response_model=List[abm_log_item])
async def cluster_details(cluster_name: str, row_count: int = 100):
    """ Get a list of logs from the ABM Cluster"""
    return logging.GetLogs(cluster_name=cluster_name, row_count=row_count)

@router.get("/urls/", response_model=abm_url_list)
async def cluster_details(cluster_name: str):
    """ This function returns list of urls per cluster after looking up from GCP Secret"""
    raw_data = gcp.get_secret_value(secret_name=cluster_name)
    result_url_list = abm_url_list()

    # Value foudn lookup value
    if raw_data:
        url_list = json.loads(raw_data)
        result_url_list.endpoint = url_list["endpoint"]
        result_url_list.dashboard = url_list["dashboard"]
        result_url_list.pages = url_list["pages"]
    
    # Return result
    return result_url_list

@router.get("/nodes/", response_model=List[AbmNode])
async def node_list(cluster_name: str, location:str):
    """ Return details of nodes in the cluster """
    return gce.get_instance_list(cluster_name=cluster_name, location=location)

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
    """ Update Cluster URLS"""
    save_value = {}
    save_value["pages"] = url_list.pages
    save_value["dashboard"] =  url_list.dashboard
    save_value["endpoint"] = url_list.endpoint

    result = gcp.set_secret_value(secret_name=cluster_name, secret_value=json.dumps(save_value))

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable To Update Token")
    else:
        return {"status":"success"}


@router.post("/set-vmlist/", responses={
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
async def set_services(cluster_name: str, vm_info: List[vm_info]):
    """ This Function saves list of VMs from inside cluster"""
    pass
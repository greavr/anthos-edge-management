from fastapi import APIRouter, HTTPException
from typing import Dict, List
import json

from core.gcp import gcp, logging, gce
from models.abm import Abm
from models.logs import abm_log_item
from models.urls import abm_url_list
from models.abm_node import AbmNode
from models.vm import vm_info

from core.settings import app_settings

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
        result_url_list.grafana = url_list["grafana"]
        result_url_list.dashboard = url_list["dashboard"]
        result_url_list.pos = url_list["pos"]
    
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
    save_value["pos"] = url_list.pos
    save_value["dashboard"] =  url_list.dashboard
    save_value["grafana"] = url_list.grafana

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
async def set_vm_list(cluster_name: str, vm_info: List[vm_info]):
    """ This Function saves list of VMs from inside cluster"""
    save_set = json.loads(gcp.get_secret_value(secret_name="vm-list"))

    for a_vm in vm_info:
        save_value = {}
        save_value["cluster_name"] = cluster_name
        save_value["vm_name"] =  a_vm.vm_name
        save_value["vm_ip"] = a_vm.vm_ip
        save_value["vm_status"] = a_vm.vm_status
        save_value["vm_image_name"] = a_vm.vm_image_name
        save_value["vm_parameter_set_name"] = a_vm.vm_parameter_set_name
        save_set.append(save_value)

    # Clean Up list
    while("" in save_set):
        save_set.remove("")
    
    result = gcp.set_secret_value(secret_name="vm-list", secret_value=json.dumps(save_set))

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable To Update VM-list")
    else:
        return {"status":"success"}

@router.get("/complete-node-list")
async def list_all_nodes():
    """ Function returns list of Anthos Baremetal Clusters in the project"""
    gce.return_instance_ip_list()
    return app_settings.node_list

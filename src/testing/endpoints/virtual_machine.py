from secrets import choice
from fastapi import APIRouter
from typing import List
import random

from core.settings import app_settings

from models.vm import vm_parameter_set, vm_image, vm_info

#APIRouter creates path operations for chaos module
router = APIRouter(
    prefix="/testing/virtual-machine",
    tags=["testing"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create-vm", responses={
     200: {
        "description": "Create Kube Virt VM",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to create virtual machine: VM_IMAGE_NAME in the cluster: CLUSTER_NAME, with parameterset: VM_PARAMETERSET_NAME"}
})
async def create_vm(vm_image_name: str, cluster_name: str, vm_parameterset_name: str = ""):
    """ This function creates a virtual machine instance : TESTING - ALWAYS SUCCESS """
    return {"status":"success"}

@router.post("/remove-vm", responses={
     200: {
        "description": "Remove Kube Virt VM",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to create virtual machine: VM_IMAGE_NAME in the cluster: CLUSTER_NAME"}
})
async def remove_vm(vm_image_name: str, cluster_name: str):
    """ This function creates a virtual machine instance : TESTING - ALWAYS SUCCESS """
    return {"status":"success"}

@router.post("/image_list", response_model=List[vm_image])
async def image_list():
    """ This function returns a list of images which can be deployed on ABM : TESTING - ALWAYS SUCCESS"""
    return app_settings.vm_machine_list

@router.post("/parameter_list", response_model=List[vm_parameter_set])
async def parameter_list():
    """ This function returns a list of parameters which can be deployed on ABM : TESTING - ALWAYS SUCCESS"""
    return app_settings.vm_parameters

@router.post("/vm_list", response_model=List[vm_info])
async def parameter_list():
    """ This function returns a list of VMs running in the entire fleet : TESTING - ALWAYS SUCCESS"""
    result_set = []
    gcp_regions = ["asia-east1","asia-east2","asia-northeast1","asia-northeast2","asia-northeast3","asia-south1","asia-south2","asia-southeast1","asia-southeast2","australia-southeast1","australia-southeast2","europeentral2","europe-north1","europe-southwest1","europe-west1-d","europe-west2","europe-west3","europe-west4","europe-west6","europe-west8","europe-west9","northamerica-northeast1","northamerica-northeast2","southamerica-east1","southamerica-west1","usentral1","us-east1-d","us-east4","us-east5","us-south1","us-west1","us-west2","us-west3","us-west4"]
    for i in range(random.randint(2, 9)):
        this_vm = vm_info(
            cluster_name= f"abm-{random.choice(gcp_regions)}",
            vm_name="vm-machine-"+str(random.randint(1, 100)),
            vm_ip="192.168.10.1",
            vm_status=random.choice(["Provisioning","Running","Stopped","Removing"]),
            vm_image_name=random.choice(app_settings.vm_machine_list).name,
            vm_parameter_set_name=random.choice(app_settings.vm_parameters).name,
        )
        result_set.append(this_vm)

    return result_set
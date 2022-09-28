import re
from fastapi import APIRouter
from typing import List

from core.settings import app_settings

from models.vm import vm_parameter_set, vm_image, vm_info

#APIRouter creates path operations for chaos module
router = APIRouter(
    prefix="/v1/virtual-machine",
    tags=["virtual-machine"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create-vm", responses={
     200: {
        "description": "Update ACM Source Repo",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to create virtual machine: VM_IMAGE_NAME in the cluster: CLUSTER_NAME, with parameterset: VM_PARAMETERSET_NAME"}
})
async def create_vm(vm_image_name: str, cluster_name: str, vm_parameterset_name: str = ""):
    """ This function creates a virtual machine instance : TESTING - ALWAYS SUCESS """
    return {"status":"success"}

@router.post("/image_list", response_model=List[vm_image])
async def image_list():
    """ This function returns a list of images which can be deployed on ABM"""
    return app_settings.vm_machine_list

@router.post("/vm_list", response_model=List[vm_info])
async def parameter_list():
    """ This function returns a list of VMs running in the entire fleet : TESTING - ALWAYS SUCESS"""
    return []

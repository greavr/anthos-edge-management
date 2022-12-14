from fastapi import APIRouter, HTTPException
from typing import List
import json

from core.settings import app_settings
from core.gcp import file_manager, git, gcp

from models.vm import vm_parameter_set, vm_image, vm_info

#APIRouter creates path operations for chaos module
router = APIRouter(
    prefix="/v1/virtual-machine",
    tags=["virtual-machine"],
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
    """ This function creates a virtual machine instance """
    create_vm = file_manager.creat_vm_file(vm_name=vm_image_name,target_cluster=cluster_name,parameter_set=vm_parameterset_name)

    if create_vm:
        return {"status":"success"}
    else:
        raise HTTPException(status_code=500, detail=f"Unable toCreate VM")

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
    """ This function creates a virtual machine instance """
    file_to_remove = f"/vms/{cluster_name}-{vm_image_name}.yaml".lower().replace("_", "-")

    if git.delete_repo_file(file_to_remove):
        return {"status":"success"}
    else:
        raise HTTPException(status_code=500, detail=f"Unable toRemove VM")

@router.get("/image_list", response_model=List[vm_image])
async def image_list():
    """ This function returns a list of images which can be deployed on ABM"""
    return app_settings.vm_machine_list

@router.get("/parameter_list", response_model=List[vm_parameter_set])
async def parameter_list():
    """ This function returns a list of parameters which can be deployed on ABM"""
    return app_settings.vm_parameters

@router.get("/vm_list", response_model=List[vm_info])
async def vm_list():
    """ This function returns a list of VMs running in the entire fleet"""
    raw_data = gcp.get_firestore_value(value_name="vm-list",collection_name="vms")
    result_vms = []

    # Value foudn lookup value
    if raw_data:
        for a_vm in raw_data["list"]:
            this_set = vm_info(
                cluster_name=a_vm["cluster_name"],
                vm_name=a_vm["vm_name"],
                vm_ip=a_vm["vm_ip"],
                vm_status=a_vm["vm_status"],
                vm_parameter_set_name=a_vm["vm_parameter_set_name"],
                vm_image_name = a_vm["vm_image_name"])
            result_vms.append(this_set)
    
    # Return result
    return result_vms

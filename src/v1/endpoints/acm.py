from asyncore import file_dispatcher
from fastapi import APIRouter, HTTPException
from typing import List

from core.gcp import acm, file_manager
from models.acm import Policy
from core.settings import app_settings

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/v1/acm",
    tags=["acm"],
    responses={404: {"description": "Not found"}},
)
@router.get("/repo", responses={
    200: {
        "description": "Repo URL",
        "content": {
            "application/json": {
                "url" : app_settings.source_repo
            }
        }
    },
    500: {"description": "Unable to find ACM repo"}
})
async def get_acm_repo():
    """ Function returns url to the Git Repo"""
    result = acm.get_source_repo()
    if not result:
        raise HTTPException(status_code=500, detail=f"Unable to find ACM repo in the project: {app_settings.gcp_project}")
    else:
        return {"url": result, }

@router.get("/policy_list", response_model=List[Policy])
async def policy_list():
    """ Return List of Available Policies"""
    return app_settings.acm_policy_list

@router.get("/application-list", responses={
    200: {
        "description": "Available Applications",
        "content": {
            "application/json": [
                {"pos_v1", "pos_v2"}
            ]
        }
    },
    500: {"description": "Unable find setting"}
})
async def application_list():
    """This function returns a list of available applications""" 
    return {"pos_v1", "pos_v2"}

@router.post("/apply-policy", responses={
    200: {
        "description": "Apply Policy",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to apply policy"}
})
async def apply_policy(labels: dict ,app_version: str = "", policy_name: str = ""):
    """ Apply Policy with labels. Body is made of Key : Value pairing of cluster labels.
    Defaults to using 'all' selector if no key:value pair set for labels"""

    if app_version == policy_name:
        raise HTTPException(status_code=418, detail="Missing either 'app_version' or 'policy_name'.")
    
    # Apply Policy
    if policy_name:
        result = file_manager.create_policy(policy_name=policy_name, target_labels=labels)

        if not result:
            raise HTTPException(status_code=500, detail=f"Unable to create policy file")
        else:
            return {"status": "success", }

    # Update app_version

    return {"status": "success", }
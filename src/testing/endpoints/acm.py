from fastapi import APIRouter, HTTPException, Query
from typing import List, Union

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
    """ Function returns url to the Git Repo : TESTING - ALWAYS SUCCESS """
    result = "https://github.com/greavr"
    if not result:
        raise HTTPException(status_code=500, detail=f"Unable to find ACM repo in the project: {app_settings.gcp_project}")
    else:
        return {"url": result, }

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
    """This function returns a list of available applications : TESTING - ALWAYS SUCCESS""" 
    return {"pos_v1", "pos_v2"}

@router.get("/policy_list", response_model=List[Policy])
async def policy_list():
    """ Return List of Available Policies : TESTING - ALWAYS SUCCESS"""
    return app_settings.acm_policy_list

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
    Defaults to using 'all' selector if no key:value pair set for labels  : TESTING - ALWAYS SUCCESS"""

    if app_version == policy_name:
        raise HTTPException(status_code=418, detail="Missing either 'app_version' or 'policy_name'.")
        
    return {"status": "success", }
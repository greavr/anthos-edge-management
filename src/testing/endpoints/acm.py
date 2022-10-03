from fastapi import APIRouter, HTTPException, Query
from typing import List, Union

from models.acm import Policy
from core.settings import app_settings

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/testing/acm",
    tags=["testing"],
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


@router.get("/policy_list", response_model=List[Policy])
async def policy_list():
    """ Return List of Available Policies"""
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
async def apply_policy(policy_name: str, target_labels: Union[List[str], None]):
    """ Apply Policy with labels : TESTING - ALWAYS SUCCESS"""
    return {"status": "success", }
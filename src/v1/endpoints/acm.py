from fastapi import APIRouter, HTTPException
from typing import List

from core.gcp import acm
from models.abm import Abm
from core.settings import app_settings

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/v1/acm",
    tags=["acm"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Abm])
async def acm_status():
    """ Function returns list of Anthos Baremetal Clusters with status in the project"""
    return acm.acm_status()

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


@router.post("/rebuild", responses={
    200: {
        "description": "Rebuild Repo",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable refresh repo"}
})
async def rebuild_repo(should_execute: bool):
    """ This function rebuilds the git repo with cluster info fround in ABM"""
    if should_execute:
        result = acm.build_repo()
        if not result:
            raise HTTPException(status_code=500, detail=f"Unable refresh repo")
        else:
            return {"status": "success", }
    else:
        raise HTTPException(status_code=500, detail=f"Did not confirm")

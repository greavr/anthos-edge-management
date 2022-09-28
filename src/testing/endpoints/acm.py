from fastapi import APIRouter, HTTPException
from typing import List

from models.abm import Abm
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
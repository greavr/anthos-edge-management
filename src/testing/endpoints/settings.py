from fastapi import APIRouter, HTTPException
from core.settings import app_settings
from core.gcp import gcp, acm, git

import logging

from typing import List

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/testing/settings",
    tags=["testing"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", responses={
    200: {
        "description": "Output Current Settings",
        "content": {
            "application/json": [
                {
                "setting_name": "example",
                "setting_value" : "example_value"
                },
                {
                "setting_name": "example2",
                "setting_value" : "example2_value"
                },]
        }
    },
    500: {"description": "Unable find setting"}
})
async def get_setting_value(setting_name: str = None):
    """ Returns setting(s) values, leaving it empty returns all values"""
    logging.debug(f"Looking for setting: {setting_name}")
    
    result = {}
    # Check for setting name
    if setting_name:
        if setting_name in app_settings.__dict__: # Check value found
            result[setting_name] = app_settings.__dict__[setting_name]
        else: # value not found
            raise HTTPException(status_code=500, detail=f"Unable to find value for: {setting_name}")
    else: # Return all
        result = app_settings.__dict__

    return result

@router.post("/git-token", responses={
    200: {
        "description": "Update Git-Token",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable To Update Token"}
})
async def set_git_token(token_value: str):
    """ Updates the git token, and stores it in the secrets vault """
    return {"status":"success"}

@router.post("/acm-repo-url", responses={
    200: {
        "description": "Update ACM Source Repo",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable To Update repo Url"}
})
async def set_repo_url(repo_url: str):
    """ Updates the git token, and stores it in the secrets vault : TESTING - ALWAYS SUCCESS """
    return {"status":"success"}

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
    """ This function rebuilds the git repo with cluster info fround in ABM : TESTING - ALWAYS SUCCESS """
    return {"status": "success", }

@router.post("/delete-repo-file", responses={
    200: {
        "description": "Delete file fromRepo",
        "content": {
            "application/json": {
                "status": "success",
                "file" : "/path/file.txt"
            }
        }
    },
    500: {"description": "Unable delete repo file"}
})
async def delete_repo_file(file_to_remove: str = ""):
    """ This function deletes either a file, or all the files in the entire repo : TESTING - ALWAYS SUCCESS"""
    raise HTTPException(status_code=500, detail=f"Unable delete repo file")

@router.get("/fleet-monitoring", response_model=List[str])
async def show_monitoring_urls():
    """ This function returns list of fleet monitoring metrics : TESTING - ALWAYS SUCCESS  """
    this_response = ["https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=6","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=2","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=4","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=8","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=10","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=16","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=18","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=20","https://grafana-cr-fljjthbteq-uc.a.run.app/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&from=1665626630153&to=1665636635057&panelId=22"]

    return this_response

@router.post("/set-fleet-monitoring", responses={
    200: {
        "description": "Update fleet-monitoring urls  : TESTING - ALWAYS SUCCESS  ",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable To fleet-monitoring urls"}
})
async def set_fleet_Urls(fleet_urls: List[str]):
    """ Updates the git token, and stores it in the secrets vault  : TESTING - ALWAYS SUCCESS  """
    return {"status":"success"}
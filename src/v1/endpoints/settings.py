import logging
from fastapi import APIRouter, HTTPException
from typing import List
from core.settings import app_settings
from core.gcp import gcp, acm, git
import json

from models.vm import vm_parameter_set, vm_image

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/v1/settings",
    tags=["settings"],
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
    logging.debug(f"Looking up setting value for: {setting_name}")
    
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
        "description": "Update Git-token",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to Update token"}
})
async def set_git_token(token_value: str):
    """ Updates the git token, and stores it in the secrets vault """
    result = gcp.set_secret_value(secret_name="git_token", secret_value=token_value) # value reflected in /src/core/settings.py

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable to Update token")
    else:
        app_settings.git_token = token_value
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
    500: {"description": "Unable to Update repo Url"}
})
async def set_repo_url(repo_url: str):
    """ Updates the git token, and stores it in the secrets vault """
    result = gcp.set_secret_value(secret_name="source_repo", secret_value=repo_url) # value reflected in /src/core/settings.py

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable to Update Repo URL")
    else:
        app_settings.source_repo = repo_url
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
    """ This function rebuilds the git repo with cluster info fround in ABM"""
    if should_execute:
        result = acm.build_repo()
        if not result:
            raise HTTPException(status_code=500, detail=f"Unable refresh repo")
        else:
            return {"status": "success", }
    else:
        raise HTTPException(status_code=500, detail=f"Did not confirm")

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
    """ This function deletes either a file, or all the files in the entire repo"""

    result = git.delete_repo_file(target_file=file_to_remove)
    if not result:
        raise HTTPException(status_code=500, detail=f"Unable delete repo file")
    else:
        return {"status": "success","file":file_to_remove }

@router.get("/fleet-monitoring", response_model=List[str])
async def show_monitoring_urls():
    """ This function returns list of fleet monitoring metrics """
    return app_settings.fleet_monitoring_urls

@router.post("/set-fleet-monitoring", responses={
    200: {
        "description": "Update fleet-monitoring urls",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to fleet-monitoring urls"}
})
async def set_fleet_Urls(fleet_urls: List[str]):
    """ Updates the git token, and stores it in the secrets vault """
    json_fleet_urls = json.dumps(fleet_urls)
    logging.debug(f"Updating fleet urls: {json_fleet_urls}")
    result = gcp.set_secret_value(secret_name="fleet_urls", secret_value=json_fleet_urls)

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable to fleet-monitoring urls")
    else:
        app_settings.fleet_monitoring_urls = fleet_urls
        return {"status":"success"}

@router.post("/set-latency-graph", responses={
    200: {
        "description": "Update latency graph url",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to latency graph url"}
})
async def set_fleet_Urls(latency_graph_url: str):
    """ Updates the git token, and stores it in the secrets vault """
    result = gcp.set_secret_value(secret_name="latency_graph_url", secret_value=latency_graph_url)

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable to latency graph url")
    else:
        app_settings.latency_graph_url = latency_graph_url
        return {"status":"success"}

@router.post("/set-looker-url", responses={
    200: {
        "description": "Update looker url",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to update looker url"}
})
async def set_looker_url(looker_url: str):
    """ Updates the git token, and stores it in the secrets vault """
    result = gcp.set_secret_value(secret_name="syncronicity_looker_url", secret_value=looker_url)

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable to update latency graph url")
    else:
        app_settings.syncronicity_looker_url = looker_url
        return {"status":"success"}
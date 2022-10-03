from fastapi import APIRouter, HTTPException
from core.settings import app_settings
from core.gcp import gcp, acm, git

from models.urls import fleet_url_list

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
    print(setting_name)
    
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
    result = gcp.set_secret_value(secret_name="git_token", secret_value=token_value) # value reflected in /src/core/settings.py

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable To Update Token")
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
    500: {"description": "Unable To Update repo Url"}
})
async def set_repo_url(repo_url: str):
    """ Updates the git token, and stores it in the secrets vault """
    result = gcp.set_secret_value(secret_name="source_repo", secret_value=repo_url) # value reflected in /src/core/settings.py

    # Successfully written
    if not result: 
        raise HTTPException(status_code=500, detail=f"Unable To Update Repo URL")
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



@router.get("/fleet-monitoring", response_model=fleet_url_list)
async def show_monitoring_urls():
    """ This function returns list of fleet monitoring metrics : TESTING - ALWAYS SUCCESS  """
    # TODO
    this_response = fleet_url_list(
        in_store_iot="http://34.170.231.75:3000/d/7vO9-x4Vz/instore-iot?orgId=1&from=1664810635205&to=1664832235205",
        fleet_hardware="http://34.170.231.75:3000/d/w0VkBx4Vz/hardware?orgId=1&from=1664810673259&to=1664832273259",
        store_wait="http://34.170.231.75:3000/d/wYOmfbV4k/store-wait?orgId=1&from=1664810709558&to=1664832309558",
        graph_list=[
            "http://34.170.231.75:3000/d-solo/k8s_views_global/kubernetes-views-global?orgId=1&refresh=30s&from=1664828762224&to=1664832362224&panelId=52",
            "http://34.170.231.75:3000/d-solo/k8s_views_global/kubernetes-views-global?orgId=1&refresh=30s&from=1664828806401&to=1664832406401&panelId=72",
            "http://34.170.231.75:3000/d-solo/k8s_views_global/kubernetes-views-global?orgId=1&refresh=30s&from=1664828835132&to=1664832435132&panelId=54",
            "http://34.170.231.75:3000/d-solo/k8s_views_global/kubernetes-views-global?orgId=1&refresh=30s&from=1664828851498&to=1664832451498&viewPanel=73"
        ]
    )

    return this_response
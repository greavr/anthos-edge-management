from fastapi import APIRouter, HTTPException
from core.settings import app_settings
from core.gcp import gcp, acm, git

from models.urls import fleet_url_list

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

@router.get("/fleet-monitoring", response_model=fleet_url_list)
async def show_monitoring_urls():
    """ This function returns list of fleet monitoring metrics : TESTING - ALWAYS SUCCESS  """
    this_response = fleet_url_list(
        overview=[
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452354605&to=1665473954605&viewPanel=2","http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452333328&to=1665473933328&theme=light&viewPanel=4"],
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452431432&to=1665474031432&viewPanel=6", "http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452510267&to=1665474110267&viewPanel=10"],
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452615358&to=1665474215358&viewPanel=12", "http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452719288&to=1665474319288&viewPanel=13","http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452759922&to=1665474359922&viewPanel=14"],
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452923822&to=1665474523822&viewPanel=16"]
        ],
        resources=[
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665452923822&to=1665474523822&viewPanel=16","http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665453275140&to=1665474875141&viewPanel=19"],
            ["http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665453347726&to=1665474947726&viewPanel=20","http://34.70.222.156:3000/d/UQ6us7S4k/overview?orgId=1&from=1665453391822&to=1665474991822&viewPanel=21"]
        ]
    )

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
async def set_fleet_Urls(fleet_urls: fleet_url_list):
    """ Updates the git token, and stores it in the secrets vault  : TESTING - ALWAYS SUCCESS  """
    return {"status":"success"}
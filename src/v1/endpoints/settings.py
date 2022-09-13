from fastapi import APIRouter, HTTPException
from core.settings import app_settings
from core.gcp import gcp

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


@router.post("/repo-url", responses={
    200: {
        "description": "Update repo-url",
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




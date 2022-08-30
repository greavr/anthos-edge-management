from fastapi import APIRouter, HTTPException
from fastapi import Query
from typing import List

import core.settings as settings
from core.gcp import gce

settings = settings.Settings()

#APIRouter creates path operations for chaos module
router = APIRouter(
    prefix="/v1/chaos",
    tags=["chaos"],
    responses={404: {"description": "Not found"}},
)


@router.post("/stopnode/", responses={
    200: {
        "description": "Instance Stopped Successfully",
        "content": {
            "application/json": {
                "example": [
                    {
                        "node_name": "abm1",
                        "node_zone": "us-central1-a",
                        "status": "stopping"
                    }
                ]
            }
        }
    },
    500: {"description": "Unable to disable node: NODE_NAME in the zone: NODE_ZONE"}
})
async def disable_node(node_zone: str, node_name: str):
    """ Disable the node """
    if not gce.stop_instance(instance_name=node_name, instance_zone=node_zone):
        raise HTTPException(status_code=500, detail=f"Unable to disable to node: {node_name} in the zone: {node_zone}")
    else:
        return {"node_name" : node_name, "node_zone": node_zone, "status": "stopping"}

@router.post("/startnode/", responses={
 200: {
        "description": "Instance Started Successfully",
        "content": {
            "application/json": {
                "example": [
                    {
                        "node_name": "abm1",
                        "node_zone": "us-central1-a",
                        "status": "starting"
                    }
                ]
            }
        }
    },
    500: {"description": "Unable to enable node: NODE_NAME in the zone: NODE_ZONE"}
})
async def enable_node(node_zone: str, node_name: str):
    """ Enable the node """
    if not gce.start_instance(instance_name=node_name, instance_zone=node_zone):
        raise HTTPException(status_code=500, detail=f"Unable to enable node: {node_name} in the zone: {node_zone}")
    else:
        return {"node_name" : node_name, "node_zone": node_zone, "status": "starting"}
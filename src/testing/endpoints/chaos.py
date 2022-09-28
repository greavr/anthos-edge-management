from fastapi import APIRouter, HTTPException
from typing import List

#APIRouter creates path operations for chaos module
router = APIRouter(
    prefix="/testing/chaos",
    tags=["testing"],
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
    """ Disable the node: TESTING - ALWAYS SUCCESS """
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
    """ Enable the node: TESTING - ALWAYS SUCCESS """
    return {"node_name" : node_name, "node_zone": node_zone, "status": "starting"}

@router.post("/disable_cluster/", responses={
    200: {
        "description": "Cluster Taken Offline",
        "content": {
            "application/json": {
                "example": [
                    {
                        "cluster_name": "abm1",
                        "location": "us-west1",
                        "status": "offline"
                    }
                ]
            }
        }
    },
    500: {"description": "Unable to disable cluster: CLUSTER_NAME in the location: CLUSTER_LOCATION"}
})
async def disable_cluster(cluster_name: str, location: str):
    """ Disable the cluster : TESTING - ALWAYS SUCCESS"""
    return {"cluster_name" : cluster_name, "location": location, "status": "offline"}

@router.post("/enable_cluster/", responses={
    200: {
        "description": "Cluster Back Online",
        "content": {
            "application/json": {
                "example": [
                    {
                        "cluster_name": "abm1",
                        "location": "us-west1",
                        "status": "online"
                    }
                ]
            }
        }
    },
    500: {"description": "Unable to enable cluster: CLUSTER_NAME"}
})
async def enable_cluster(cluster_name: str):
    """ Enable the cluster : TESTING - ALWAYS SUCCESS """
    return {"cluster_name" : cluster_name, "status": "online"}


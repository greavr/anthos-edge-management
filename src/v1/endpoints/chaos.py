from fastapi import APIRouter, HTTPException
from typing import List

import core.settings as settings
from core.gcp import gce, network

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
    """ Disable the cluster """
    if not network.disable_network(cluster=cluster_name, location=location):
        raise HTTPException(status_code=500, detail=f"Unable to disable cluster: {cluster_name} in the location: {location}")
    else:
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
    """ Enable the cluster """
    if not network.enable_network(cluster=cluster_name):
        raise HTTPException(status_code=500, detail=f"Unable to disable cluster: {cluster_name} ")
    else:
        return {"cluster_name" : cluster_name, "status": "online"}


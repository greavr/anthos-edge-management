from fastapi import APIRouter, HTTPException
from core.settings import app_settings

import logging

from typing import List

#APIRouter creates path operations for settings module
router = APIRouter(
    prefix="/v1/synchronicity",
    tags=["synchronicity"],
    responses={404: {"description": "Not found"}},
)

@router.get("/latency-graph", response_model=str)
async def latency_graph():
    """ This function returns URL to the Latency Graph """
    return app_settings.latency_graph_url

@router.get("/looker-dashboard", response_model=str)
async def looker_dashboard():
    """ This function returns URL to the Syncronicity looker dashboard """
    return app_settings.syncronicity_looker_url

@router.post("/set-cluster-latency", responses={
    200: {
        "description": "Set Cluster Latency for synchronicity",
        "content": {
            "application/json": {
                "status": "success"
            }
        }
    },
    500: {"description": "Unable to set cluster latency"}
})
async def set_cluster_latency(cluster_name: str, latency_value: int):
    """ This function configures latency for cluster data to sync data to Google Cloud"""
    return {"status":"success"}
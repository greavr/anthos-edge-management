from fastapi import APIRouter
from fastapi import Query
from typing import List

from core.gcp import gcp, logging
from models.abm import Abm
from models.logs import abm_log_item
from models.urls import abm_url_list
import core.settings as settings

settings = settings.Settings()

#APIRouter creates path operations for abm module
router = APIRouter(
    prefix="/v1/abm",
    tags=["abm"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Abm])
async def list_of_abm_clusters():
    """ Function returns list of Anthos Baremetal Clusters in the project"""
    return gcp.get_abm_list()


@router.get("/logs/{cluster_name}", response_model=List[abm_log_item])
async def cluster_details(cluster_name: str):
    """ Get a list of logs from the ABM Cluster"""
    return logging.GetLogs(cluster_name=cluster_name)

@router.get("/urls/{cluster_name}", response_model=abm_url_list)
async def cluster_details(cluster_name: str):
    return {}
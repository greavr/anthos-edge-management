from typing import Dict
from core.settings import app_settings
import logging
import csv
import cachetools.func

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

def Configure_Logging():
    """ Function to build logging"""
    logging.basicConfig(level=logging.INFO)
    # client = google.cloud.logging.Client()
    # handler = CloudLoggingHandler(client)
    # logging.getLogger().setLevel(logging.DEBUG)
    # setup_logging(handler)

@cachetools.func.ttl_cache(maxsize=128, ttl=60)
def lookup_location(gcp_region: str) -> Dict[str,str]:
    """ This function returns x,y co-ordinates or returns random land location if not found"""
    result = {"latitude" : "0 0 N", "longitude" : "0 0 W"}

    # Build results
    with open(app_settings.region_file) as f:
        reader = csv.DictReader(f)

        # Check if value exists
        for aItem in reader:
            if aItem["location"] == gcp_region:
                result["latitude"] = aItem["latitude"]
                result["longitude"] = aItem["longitude"]
                   
    return result
    
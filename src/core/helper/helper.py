import core.settings as settings
import os
import logging
import sys

import google.cloud.logging

def Configure_Logging():
    """ Function to build logging"""

    client = google.cloud.logging.Client()

    client.setup_logging()

## Helper functions
def GetConfig():
    # Function to Open config.json file and load values
    try:
        # Set Variables
        settings.gcp_project = os.environ.get('GCP_PROJECT', '')
        print(settings.gcp_project)
    except Exception as e:
        # Unable to load file, quit
        logging.error(f"Problem loading environmental variables")
        logging.error(e)
        quit()
import core.settings as settings
import os
import logging
import sys

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

def Configure_Logging():
    """ Function to build logging"""
    #logging.basicConfig(level=logging.DEBUG)
    client = google.cloud.logging.Client()
    handler = CloudLoggingHandler(client)
    logging.getLogger().setLevel(logging.DEBUG)
    setup_logging(handler)
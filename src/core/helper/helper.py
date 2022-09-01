import core.settings as settings
import os
import logging
import sys

import google.cloud.logging

def Configure_Logging():
    """ Function to build logging"""

    client = google.cloud.logging.Client()

    client.setup_logging()
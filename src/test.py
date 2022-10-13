from core.helper import helper

from core.gcp import gcp, git, acm, gce

print(gce.get_instance_list(location="us-west1"))

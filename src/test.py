from core.helper import helper

from core.gcp import gcp, git, acm, gce, file_manager

# Build VM List
helper.build_vm_info()
helper.build_policy_list()

print(gcp.get_abm_list())

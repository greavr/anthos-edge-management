from core.helper import helper

from core.gcp import gcp, git, acm, gce, file_manager

# Build VM List
helper.build_vm_info()

# Build Policy List
helper.build_policy_list()

print(file_manager.creat_vm_file(vm_name="Windows_10",target_cluster="abm-europe-west1", parameter_set="windows_10_a"))

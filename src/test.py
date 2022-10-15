from core.helper import helper

from core.gcp import gcp, git, acm, gce, file_manager

# Build VM List
helper.build_vm_info()

# Build Policy List
helper.build_policy_list()
labels = {
    "canary": ["10"],
}

print(acm.update_application(labels=labels,app_name="pos_v1"))

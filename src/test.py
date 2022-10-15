from core.helper import helper

from core.gcp import gcp, git, acm, gce, file_manager

# Build VM List
helper.build_vm_info()

# Build Policy List
helper.build_policy_list()
labels = {
    "continent": ["asia", "europe", "australia"],
    "canary": ["10", "25", "50"],
}

print(file_manager.create_policy(policy_name="require-repo-is-gcr",target_labels=labels))

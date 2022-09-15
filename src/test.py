from core.gcp import git, acm, file_manager
import logging

logging.basicConfig(level=logging.INFO)

print(git.delete_repo_file())
print(acm.build_repo())
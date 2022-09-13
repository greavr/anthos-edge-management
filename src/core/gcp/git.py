import logging
from typing import List
from github import Github
from urllib.parse import urlparse

from core.settings import app_settings

def get_repos():
    g = Github(app_settings.git_token)
    repo_list = g.get_user().get_repos()
    for repo in repo_list:
        print(repo)
        print(f"{repo.full_name} - {repo.default_branch}")


    return repo_list

def get_branches(repo_name: str):
    g = Github(app_settings.git_token)
    repo = g.get_repo(repo_name)

    branch_list = repo.get_branches()

    for branch in branch_list:
        print(branch)
        print(branch.name)

def add_file_to_branch(file_list: List[str]) -> list[str]:
    """ This function writes files to the git repo (Sadly one at a time)"""
    uploaded_files = []
    try:
        g = Github(app_settings.git_token)

        # Parse the target repo
        repo_name = urlparse(app_settings.source_repo).path[1:]
        logging.debug(f"Repo name: {repo_name}")

        repo = g.get_repo(repo_name)

        for afile in file_list:
            try:
                file_name = f"{afile.rsplit('/')[-2]}/{afile.rsplit('/')[-1]}"
                logging.debug(f"Reading file: {file_name}")
                #open text file in read mode
                with open(afile, 'r') as f:
                    filecontents = f.read()
                repo.create_file(file_name, f"Adding: {file_name}", str(filecontents) , branch="main")
                uploaded_files.append(file_name)
            except Exception as e:
                logging.error(e)
                print(e)

    except Exception as e:
        logging.error(e)
        print(e)

    return uploaded_files
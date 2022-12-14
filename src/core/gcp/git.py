import logging
from typing import List
from pathlib import Path
from github import Github
from urllib.parse import urlparse

from core.settings import app_settings

def get_repos():
    g = Github(app_settings.git_token)
    repo_list = g.get_user().get_repos()
    for repo in repo_list:
        logging.debug(repo)
        logging.info(f"{repo.full_name} - {repo.default_branch}")


    return repo_list

def get_branches(repo_name: str) -> List[str]:
    """ This function returns list of git branchs on the repo"""
    g = Github(app_settings.git_token)
    repo = g.get_repo(repo_name)

    results = []

    branch_list = repo.get_branches()

    for branch in branch_list:
        logging.debug(branch)
        results.append(branch.name)

    return results

def get_contents(file_path: str) -> str:
    """ This function returns the contents of a file on git"""
    result = None
    try:
        g = Github(app_settings.git_token)

        repo_name = urlparse(app_settings.source_repo).path[1:]
        logging.debug(f"Repo name: {repo_name}")

        repo = g.get_repo(repo_name)

        contents = repo.get_contents(file_path)

        result = contents.decoded_content.decode('utf-8')

    except Exception as e:
                logging.error(e)
                logging.error(e)

    return result

def check_file(file_path: str) -> str:
    """ This function checks if the file exists in git, if so returns the SHA"""

    result = None
    try:
        g = Github(app_settings.git_token)

        repo_name = urlparse(app_settings.source_repo).path[1:]
        logging.debug(f"Repo name: {repo_name}")

        repo = g.get_repo(repo_name)

        contents = repo.get_contents(file_path)

        result = contents.sha

    except Exception as e:
                logging.error(e)
                logging.error(e)

    return result
    
def add_file_to_branch(file_list: List[str]) -> list[str]:
    """ This function writes files to the git repo (Sadly one at a time)"""
    uploaded_files = []

    # Remove dupes on large file list
    clean_list = [*set(file_list)]


    logging.debug(clean_list)
    try:
        g = Github(app_settings.git_token)

        # Parse the target repo
        repo_name = urlparse(app_settings.source_repo).path[1:]
        logging.debug(f"Repo name: {repo_name}")

        repo = g.get_repo(repo_name)

        for afile in clean_list:
            try:
                file_name_raw = Path(afile).parts
                file_name = str(Path(*file_name_raw[file_name_raw.index("files")+1:]))

                #open text file in read mode
                with open(afile, 'r') as f:
                    filecontents = f.read()

                # Check file is on repo
                file_exist_sha = check_file(file_path=file_name)

                if file_exist_sha:
                    logging.debug(f"Updating file in repo file: on-disk-file: {afile}, git-path: {file_name}, contents: {filecontents[0:10]}..")
                    repo.update_file(path=file_name, sha=file_exist_sha, content=filecontents, message=f"Adding: {file_name}", branch="main")
                else:
                    logging.debug(f"Adding file: on-disk-file: {afile}, git-path: {file_name}, contents: {filecontents[0:10]}..")
                    repo.create_file(path=file_name, content=filecontents, message=f"Adding: {file_name}", branch="main")
                uploaded_files.append(file_name)

            except Exception as e:
                logging.error(e)
                logging.error(e)

    except Exception as e:
        logging.error(e)
        logging.error(e)

    return uploaded_files

def get_copy_from_file_contents() -> dict[str,str]:
    """ This function returns a list of files and their contents from the repo"""

    file_list = {}
    g = Github(app_settings.git_token)
    repo = g.get_repo(app_settings.copy_from_repo)
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if (".yaml" in file_content.name) and not ("cloudbuild" in file_content.name ):                
                file_list[file_content.path] = file_content.decoded_content.decode('utf-8')

    
    return file_list

def delete_repo_file(target_file: str = "") -> bool:
    """ This function removes a specific file from the repo """
    result = False
    try:
        # Remove the files
        g = Github(app_settings.git_token)
        repo = g.get_repo(urlparse(app_settings.source_repo).path[1:])

        if target_file:
            contents = [repo.get_contents(target_file)]
        else:
            contents = repo.get_contents(target_file)

        logging.debug(f"File contents: {contents}")
        while contents:
            file_content = contents.pop(0)
            logging.debug(f"removing file: {file_content.name}")

            # Ignore folder
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                # Delete file
                repo.delete_file(file_content.path ,f"Removing: {file_content.name}", file_content.sha, branch="main")

        result = True
    except Exception as e:
        logging.error(e)
        logging.error(e)

    return result
from core.gcp import git


file_list = ['src/core/gcp/files/setup/abm-us-east4.yaml', 'src/core/gcp/files/abm-us-east4/repo-sync.yaml', 'src/core/gcp/files/abm-us-east4/repo-rbac.yaml', 'src/core/gcp/files/selectors/abm-us-east4-sel.yaml', 'src/core/gcp/files/selectors/state-virginia-sel.yaml', '', '', 'src/core/gcp/files/selectors/loc-us-east4-sel.yaml']
while("" in file_list):
    file_list.remove("")
git.add_file_to_branch(file_list=file_list)
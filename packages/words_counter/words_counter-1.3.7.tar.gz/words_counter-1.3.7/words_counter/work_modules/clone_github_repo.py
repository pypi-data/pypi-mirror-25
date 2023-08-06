from git import Repo


def clone_repo_from_github(url_and_pathway):
    url = url_and_pathway[0]
    pathway = url_and_pathway[1]
    Repo.clone_from(url, pathway)

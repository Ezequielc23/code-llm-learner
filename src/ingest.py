import os
from git import Repo

def import_repo(repo_url_or_path, output_dir="temp_repo"):
    """Clone a repo or copy local directory."""
    if os.path.exists(repo_url_or_path):
        repo_path = repo_url_or_path
    else:
        repo_path = output_dir
        Repo.clone_from(repo_url_or_path, repo_path)
    return repo_path

def read_codebase(repo_path):
    """Read all code files into a dictionary."""
    codebase = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".cpp", ".java")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    codebase[file_path] = f.read()
    return codebase

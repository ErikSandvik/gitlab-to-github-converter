import subprocess
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv('GITHUB_TOKEN')
github_user = os.getenv('GITHUB_USER')


def create_repository(repo_name):
    url = "https://api.github.com/user/repos"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "name": repo_name,
        "private": True
    }

    response = requests.post(url, headers=headers, json=params)

    if not response.ok:
        raise Exception(f"GitHub repo creation failed: {response.status_code} {response.text}")

    return response


def push_to_github(repo_name):
    root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(root)
    clone_dir = os.path.join(project_root, "cloned_projects")
    repo_path = os.path.join(clone_dir, repo_name)

    if not os.path.isdir(f"{clone_dir}/{repo_name}"):
        raise FileNotFoundError("Repository does not exist locally")

    subprocess.run(["git", "remote", "add", "github",
                    f"https://{github_token}@github.com/{github_user}/{repo_name}.git"],
                   cwd=repo_path)
    subprocess.run(["git", "push", "--set-upstream", "github", "main"], cwd=repo_path)


def push_project_list_to_github(project_list):
    for project_name in project_list:
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '-', project_name)
        create_repository(safe_name)
        push_to_github(safe_name)

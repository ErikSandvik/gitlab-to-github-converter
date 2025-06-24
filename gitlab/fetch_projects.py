import os
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

def load_gitlab_token():
    gitlab_token = os.getenv("GITLAB_TOKEN")

    if gitlab_token is None:
        raise ValueError("GITLAB_TOKEN environment variable is not set")

    return gitlab_token


def get_projects(gitlab_host, access_token):
    headers = {"PRIVATE-TOKEN": access_token}

    page = 1
    projects = []
    while True:
        params = {"page": page, "per_page": 100, "membership": True}
        response = requests.get(f"https://{gitlab_host}/api/v4/projects", headers=headers, params=params)
        if not response.ok:
            raise InterruptedError("Error fetching projects: " + str(response.text))

        page_projects = response.json()

        if not page_projects:
            return projects

        projects.extend(page_projects)
        page += 1


def locally_clone_project(gitlab_https, access_token, target_folder):
    subprocess.run(["git", "clone", f"https://oauth2:{access_token}@{gitlab_https}"], cwd=target_folder)


def locally_clone_project_list(gitlab_https_list, access_token, target_folder):
    for https_address in gitlab_https_list:
        locally_clone_project(https_address, access_token, target_folder)


def fetch_and_locally_clone_projects(gitlab_host, access_token, target_folder):
    gitlab_projects = get_projects(gitlab_host, access_token)
    https_for_projects = get_https_from_json_list(gitlab_projects)
    locally_clone_project_list(https_for_projects, access_token, target_folder)


def get_https_from_json_list(project_json_list):
    https_list = []
    for project_json in project_json_list:
        https_list.append(project_json["http_url_to_repo"][len("https://"):])
    return https_list

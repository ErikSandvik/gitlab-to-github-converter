import os
import requests
from dotenv import load_dotenv

load_dotenv()


def load_gitlab_token():
    gitlab_token = os.getenv("GITLAB_TOKEN")

    if gitlab_token is None:
        return ValueError("GITLAB_TOKEN environment variable is not set")

    return gitlab_token


def get_projects(gitlab_host):
    gitlab_token = load_gitlab_token()
    headers = {"PRIVATE-TOKEN": gitlab_token}

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


if __name__ == "__main__":
    host = "gitlab.stud.idi.ntnu.no"
    returned_projects = get_projects(host)

import os
import requests
import subprocess
from dotenv import load_dotenv


class GitlabFetcher:
    def __init__(self):
        load_dotenv()
        self.gitlab_host = os.getenv('GITLAB_HOST')
        self.gitlab_token = os.getenv('GITLAB_TOKEN')
        self.project_list = []

        if not self.gitlab_host or not self.gitlab_token:
            raise ValueError("Missing GITLAB_HOST or GITLAB_TOKEN in environment.")

    def fetch_projects(self):
        headers = {"PRIVATE-TOKEN": self.gitlab_token}

        page = 1
        projects = []
        while True:
            params = {"page": page, "per_page": 100, "membership": True}
            response = requests.get(f"https://{self.gitlab_host}/api/v4/projects", headers=headers, params=params)
            if not response.ok:
                raise InterruptedError("Error fetching projects: " + str(response.text))

            page_projects = response.json()

            if not page_projects:
                self.project_list = projects
                return

            projects.extend(page_projects)
            page += 1

    def locally_clone_project(self, gitlab_https, target_folder):
        subprocess.run(["git", "clone", f"https://oauth2:{self.gitlab_token}@{gitlab_https}"], cwd=target_folder)

    def locally_clone_project_list(self, gitlab_https_list, target_folder):
        os.makedirs(target_folder, exist_ok=True)
        for https_address in gitlab_https_list:
            self.locally_clone_project(https_address, target_folder)

    def fetch_and_locally_clone_projects(self, target_folder):
        self.fetch_projects()
        self.locally_clone_project_list(self.get_https_from_json_list(), target_folder)

    def get_https_from_json_list(self):
        https_list = []
        for project_json in self.project_list:
            https_list.append(project_json["http_url_to_repo"][len("https://"):])
        return https_list

    def get_names_from_json_list(self):
        names_list = []
        for project_json in self.project_list:
            names_list.append(project_json["name"])
        return names_list

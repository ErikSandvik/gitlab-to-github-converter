import os

from dotenv import load_dotenv

from gitlab.gitlab_fetcher import GitlabFetcher
from github.github_pusher import push_project_list_to_github


def check_if_environment_variables():
    load_dotenv()
    if os.getenv("GITHUB_TOKEN") is None:
        print("GITHUB_TOKEN environment variable not set")
        return False
    if os.getenv("GITHUB_USER") is None:
        print("GITHUB_USER environment variable not set")
        return False
    if os.getenv("GITLAB_TOKEN") is None:
        print("GITLAB_TOKEN environment variable not set")
        return False
    return True


def convert_gitlab_projects_to_github():
    project_root = os.path.dirname(os.path.abspath(__file__))
    clone_dir = os.path.join(project_root, "cloned_projects")

    gitlab_fetcher = GitlabFetcher()
    gitlab_fetcher.fetch_and_locally_clone_projects(clone_dir)
    push_project_list_to_github(gitlab_fetcher.get_names_from_json_list())


def main():
    if check_if_environment_variables():
        convert_gitlab_projects_to_github()


if __name__ == '__main__':
    main()

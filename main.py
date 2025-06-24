import os

from dotenv import load_dotenv

from gitlab.fetch_projects import fetch_and_locally_clone_projects

load_dotenv()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def load_gitlab_token():
    gitlab_token = os.getenv("GITLAB_TOKEN")

    if gitlab_token is None:
        raise ValueError("GITLAB_TOKEN environment variable is not set")

    return gitlab_token


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    folder_path = r"cloned_projects"
    host = "gitlab.stud.idi.ntnu.no"
    fetch_and_locally_clone_projects(host, load_gitlab_token(), folder_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

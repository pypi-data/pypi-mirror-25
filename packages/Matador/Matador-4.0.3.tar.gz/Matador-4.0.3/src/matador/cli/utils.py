from logging import getLogger
import shutil
from configparser import ConfigParser
from pathlib import Path

import yaml
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo

from matador import git

logger = getLogger(__name__)


def deployment_repository(project_folder):
    project = Path(project_folder).name
    deployment_folder = Path(Path.home(), '.matador', project)
    deployment_repo_folder = Path(deployment_folder, 'repository')

    Path.mkdir(deployment_folder, parents=True, exist_ok=True)
    Path.mkdir(deployment_repo_folder, parents=True, exist_ok=True)

    try:
        repo = Repo(str(deployment_repo_folder))
    except NotGitRepository:
        config_file = Path(deployment_repo_folder, '.git', 'config')
        config = ConfigParser()

        repo = Repo.init(str(deployment_repo_folder))
        config.read(str(config_file))

        config['core']['sparsecheckout'] = 'true'
        config['remote "origin"'] = {
            'url': project_folder.as_posix(),
            'fetch': '+refs/heads/*:refs/remotes/origin/*'
        }

        with config_file.open('w') as f:
            config.write(f)

        sparse_checkout_file = Path(
            deployment_repo_folder, '.git', 'info', 'sparse-checkout')
        with sparse_checkout_file.open('a') as f:
            f.write('/src\n')
            f.write('/deploy\n')

    return repo


def ticket_deployment_folder(environment, ticket, commit, packaged):
    project_repo = Repo.discover()
    project_folder = Path(project_repo.path)
    project = project_folder.name
    ticket_deployment_folder = Path(
        Path.home(), '.matador', project, environment, 'tickets', ticket)
    if commit is None:
        commit = project_repo.head().decode(encoding='ascii')
    deployment_repo = deployment_repository(project_folder)
    ticket_src_folder = Path(deployment_repo.path, 'deploy', 'tickets', ticket)
    if not packaged:
        git.fetch_all(project_repo, deployment_repo)

    shutil.rmtree(str(ticket_deployment_folder), ignore_errors=True)
    git.checkout(deployment_repo, commit)
    shutil.copytree(str(ticket_src_folder), str(ticket_deployment_folder))
    return ticket_deployment_folder


def package_definition(environment, package, commit):
    project_repo = Repo.discover()
    project_folder = Path(project_repo.path)
    project = project_folder.name
    package_deployment_folder = Path(
        Path.home(), '.matador', project, environment, 'packages', package)
    deployment_repo = deployment_repository(project_folder)
    package_src_folder = Path(
        deployment_repo.path, 'deploy', 'packages', package)

    git.fetch_all(project_repo, deployment_repo)
    shutil.rmtree(str(package_deployment_folder), ignore_errors=True)
    git.checkout(deployment_repo, commit)
    shutil.copytree(str(package_src_folder), str(package_deployment_folder))
    tickets_file = Path(package_deployment_folder, 'tickets.yml')
    return tickets_file


def environments():
    project_folder = Path(Repo.discover().path)
    file_path = Path(
        project_folder, 'config', 'environments.yml')
    try:
        file = file_path.open('r')
        environments = yaml.load(file)
        if environments:
            return environments
        else:
            raise ValueError()
    except FileNotFoundError:
        logger.error('Cannot find environments.yml file')
    except ValueError:
        logger.error('environments.yml exists but is empty')


def credentials():
    project_folder = Path(Repo.discover().path)
    file_path = Path(
        project_folder, 'config', 'credentials.yml')
    try:
        file = file_path.open('r')
        credentials = yaml.load(file)
        if credentials:
            return credentials
        else:
            raise ValueError()
    except FileNotFoundError:
        logger.error('Cannot find credentials.yml file')
    except ValueError:
        logger.error('credentials.yml exists but is empty')

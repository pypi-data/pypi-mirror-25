import logging
import os
import shutil
from pathlib import Path

from dulwich.repo import Repo
from openpyxl import load_workbook

import matador.cli.utils as utils
import matador.session as session
from matador import git
from matador import zippey

logger = logging.getLogger(__name__)


def _create_deployment_xlsx_file(source_file, deployment_file, commit_ref):
    """Copy a source .xlsx file to the deployment folder and add git info its
    file properties.
    """
    project = Path(Repo.discover().path).name
    repo_folder = Path(Path.home(), '.matador', project, 'repository')
    repo = Repo(str(repo_folder))

    version, commit_timestamp, author = git.keyword_values(repo, commit_ref)

    deployment_file.touch()
    zippey.decode(source_file.open('rb'), deployment_file.open('wb'))

    workbook = load_workbook(str(deployment_file))
    workbook.properties.creator = author
    workbook.properties.version = version
    workbook.save(str(deployment_file))


def _create_deployment_text_file(source_file, deployment_file, commit_ref):
    """Copy a source text file to the deployment folder and perform git keyword
    substitution on the copy.
    """
    project = Path(Repo.discover().path).name
    repo_folder = Path(Path.home(), '.matador', project, 'repository')
    repo = Repo(str(repo_folder))

    with source_file.open('r') as f:
        original_text = f.read()

    new_text = git.substitute_keywords(original_text, repo, commit_ref)

    with deployment_file.open('w') as f:
        f.write(new_text)


create_deployment_file = {
    '.xlsx': _create_deployment_xlsx_file,
    '.arw': _create_deployment_text_file,
    '.rpx': _create_deployment_text_file,
}


def deploy_report_file(report_name, report_file_name, commit_ref):
    """Checkout a report file from the matador repo, copy it to the deployment
    folder, add git keywords to the copy and deploy the result to the ABW
    Customised Reports folder.
    """
    project = Path(Repo.discover().path).name
    repo_folder = Path(Path.home(), '.matador', project, 'repository')
    repo = Repo(str(repo_folder))
    deployment_folder = Path(
        Path.home(), '.matador', project, session.environment, 'tickets',
        session.ticket)

    source_file = Path(
        repo_folder, 'src', 'reports', report_name, report_file_name)
    deployment_file = Path(deployment_folder, report_file_name)

    # I've been unable to get UNC shares working as Path objects, so I'm
    # using a simple string here. Also, that's what shutil requires anyway.
    environment = utils.environments()[session.environment]
    target_folder = (
        '//' +
        environment['abwServer'] + '/' +
        environment['customisedReports'])

    git.checkout(repo, commit_ref)
    create_deployment_file[source_file.suffix](
        source_file, deployment_file, commit_ref)
    logger.info(f'Deploying {report_file_name} to {target_folder}')
    shutil.copy(str(deployment_file), target_folder)


def remove_report_file(report_file_name):
    """Remove a report file from the ABW Customised Reports Folder"""
    environment = utils.environments()[session.environment]
    target_folder = (
        '//' +
        environment['abwServer'] + '/' +
        environment['customisedReports'])
    target_file = target_folder + '/' + report_file_name
    logger.info(f'Removing {report_file_name} from {target_folder}')
    try:
        os.remove(target_file)
    except FileNotFoundError:
        logger.info(f'{report_file_name} does not exist in {target_folder}')

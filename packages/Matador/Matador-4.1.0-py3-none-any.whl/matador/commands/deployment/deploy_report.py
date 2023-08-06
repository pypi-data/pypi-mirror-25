import logging
import os
from pathlib import Path
from matador.session import Session
from matador import git
from matador import zippey
import shutil
from openpyxl import load_workbook


def _create_deployment_xlsx_file(source_file, deployment_file, commit_ref):
    """Copy a source .xlsx file to the deployment folder and add git info its
    file properties.
    """
    version, commit_timestamp, author = git.keyword_values(
        Session.matador_repo, commit_ref)

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
    with source_file.open('r') as f:
        original_text = f.read()

    new_text = git.substitute_keywords(
        original_text, Session.matador_repo, commit_ref)

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
    logger = logging.getLogger(__name__)
    source_file = Path(
        Session.matador_repository_folder, 'src', 'reports', report_name,
        report_file_name)
    deployment_file = Path(Session.deployment_folder, report_file_name)

    # I've been unable to get UNC shares working as Path objects, so I'm
    # using a simple string here. Also, that's what shutil requires anyway.
    target_folder = (
        '//' +
        Session.environment['abwServer'] + '/' +
        Session.environment['customisedReports'])

    git.checkout(Session.matador_repo, commit_ref)
    create_deployment_file[source_file.suffix](
        source_file, deployment_file, commit_ref)
    logger.info(f'Deploying {report_file_name} to {target_folder}')
    shutil.copy(str(deployment_file), target_folder)


def remove_report_file(report_file_name):
    """Remove a report file from the ABW Customised Reports Folder"""
    logger = logging.getLogger(__name__)
    target_folder = (
        '//' +
        Session.environment['abwServer'] + '/' +
        Session.environment['customisedReports'])
    target_file = target_folder + '/' + report_file_name
    logger.info(f'Removing {report_file_name} from {target_folder}')
    try:
        os.remove(target_file)
    except FileNotFoundError:
        logger.warning(f'{report_file_name} does not exist in {target_folder}')

import io
from logging import getLogger
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import click
import yaml
from cookiecutter.main import cookiecutter
from dulwich.repo import Repo

import matador.cli.utils as utils
from matador import git
from matador import logging
from matador import zippey
from matador.cli import sql
from matador.cli.decorators import deploys_changes
from matador.cli.decorators import windows_only

logger = getLogger(__name__)


@click.version_option(message='%(prog)s %(version)s :: Empiria Ltd')
@click.group()
@click.option(
    '--log', '-l', default='console', help='Logging Destination',
    type=click.Choice(['console', 'file']))
@click.option('--verbosity', '-v', default='info', help='Logging verbosity')
def matador(log, verbosity):
    logging.setup(log, verbosity)


@matador.command(name='init')
@click.option('--project', '-p', prompt='Project Name', help='Project Name')
def create_project(project):
    """Create the folder structure for a new matador project

    A new folder will be created beneath the current working folder, using the
    project name provided, and the matador folder structure will reside beneath
    that.
    """
    cookiecutter(
        'https://github.com/Empiria/matador-cookiecutter.git',
        no_input=True,
        extra_context={'project_name': project})
    logger.info(f'Created matador project {project}')


@matador.command(name='create-ticket')
@click.option('--ticket', '-t', prompt='Ticket', help='Ticket Name')
def create_ticket(ticket):
    """Create the folder, deployment and removal files for a ticket beneath
    the project's 'deploy' folder and commit that change."""
    project_repo = Repo.discover()
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', ticket)
    Path.mkdir(ticket_folder, parents=True, exist_ok=True)

    for file_name in ('deploy.py', 'remove.py'):
        file = Path(ticket_folder, file_name)
        with file.open('w') as f:
            f.write('from matador.deployment import *\n\n')
        git.stage_file(project_repo, file)

    git.commit(project_repo, f'Create ticket {ticket}')
    logger.info(f'Created ticket {ticket}')


@matador.command(name='create-package')
@click.option('--package', '-p', prompt='Package', help='Package Name')
def create_package(package):
    """Create the folder and definition file for a package beneath the
    project's 'deploy' folder and commit that change."""
    project_repo = Repo.discover()
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    Path.mkdir(package_folder, parents=True, exist_ok=True)

    package_file = Path(package_folder, 'tickets.yml')
    with package_file.open('w') as f:
        f.write(
            '# List each ticket on a separate line preceded by - . e.g.\n')
        f.write('# - 30\n')
        f.write('# - 31\n')
    git.stage_file(project_repo, package_file)

    remove_file = Path(package_folder, 'remove.py')
    with remove_file.open('w') as f:
        f.write('from matador.deployment import *\n\n')

    git.stage_file(project_repo, remove_file)
    git.commit(project_repo, f'Create package {package}')
    logger.info(f'Created package {package}')


@matador.command(name='add-t2p')
@click.option('--ticket', '-t', prompt='Ticket', help='Ticket Name')
@click.option('--package', '-p', prompt='Package', help='Package Name')
def add_ticket_to_package(ticket, package):
    """Add a ticket to the definition file for a package and commit that
    change."""
    project_repo = Repo.discover()
    package_file = Path(
        project_repo.path, 'deploy', 'packages', package, 'tickets.yml')

    with package_file.open('a') as f:
        f.write(f'- {ticket}\n')

    git.stage_file(project_repo, package_file)
    git.commit(project_repo, f'Add ticket {ticket} to package {package}')
    logger.info(f'Added ticket {ticket} to package {package}')


@matador.command(name='deploy-ticket')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--ticket', '-t', prompt='Ticket', help='Ticket Name')
@click.option('--commit', '-c', default=None, help='Commit Reference')
@click.option('--packaged', '-p', is_flag=True, default=False)
@deploys_changes
def deploy_ticket(environment, ticket, commit, packaged):
    """Excecute the deployment file for the given ticket against the given
    environment."""
    logger.info(f'Deploying ticket {ticket} to {environment}')
    try:
        deployment_folder = utils.ticket_deployment_folder(
            environment, ticket, commit, packaged)
        source_file = Path(deployment_folder, 'deploy.py')
        SourceFileLoader('deploy', str(source_file)).load_module()
    except FileNotFoundError:
        logger.error(f'Cannot find deployment folder/file for ticket {ticket}')


@matador.command(name='remove-ticket')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--ticket', '-t', prompt='Ticket', help='Ticket Name')
@click.option('--commit', '-c', default=None, help='Commit Reference')
@click.option('--packaged', '-p', is_flag=True, default=False)
@deploys_changes
def remove_ticket(environment, ticket, commit, packaged):
    """Excecute the removal file for the given ticket against the given
    environment."""
    logger.info(f'Removing ticket {ticket} from {environment}')
    try:
        deployment_folder = utils.ticket_deployment_folder(
            environment, ticket, commit, packaged)
        source_file = Path(deployment_folder, 'remove.py')
        SourceFileLoader('remove', str(source_file)).load_module()
    except FileNotFoundError:
        logger.error(f'Cannot find deployment folder/file for ticket {ticket}')

@matador.command(name='deploy-package')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--package', '-p', prompt='Package', help='Package Name')
@click.option('--commit', '-c', default=None, help='Commit Reference')
def deploy_package(environment, package, commit):
    """Execute the deployment file for each ticket listed in the definition
    file for the given package."""
    logger.info(f'Deploying package {package} to {environment}')
    try:
        tickets_file = utils.package_definition(environment, package, commit)
    except FileNotFoundError:
        logger.error(
            f'Cannot find definition folder/file for package {package}')
        return

    with tickets_file.open('r') as f:
        for ticket in yaml.load(f):
            logger.info('*' * 25)
            logger.info(f'Deploying ticket {ticket} to {environment}')
            try:
                deployment_folder = utils.ticket_deployment_folder(
                    environment, ticket, commit, True)
                source_file = Path(deployment_folder, 'deploy.py')
                SourceFileLoader('deploy', str(source_file)).load_module()
            except FileNotFoundError:
                logger.error(
                    f'Cannot find deployment folder/file for ticket {ticket}')


@matador.command(name='remove-package')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--package', '-p', prompt='Package', help='Package Name')
@click.option('--commit', '-c', prompt='Commit Ref', help='Commit Reference')
def remove_package(environment, package, commit):
    """Execute the removal file for each ticket listed in the definition
    file for the given package."""
    logger.info(f'Removing package {package} from {environment}')
    try:
        tickets_file = utils.package_definition(environment, package, commit)
    except FileNotFoundError:
        logger.error(
            f'Cannot find definition folder/file for package {package}')
        return

    with tickets_file.open('r') as f:
        for ticket in yaml.load(f):
            logger.info('*' * 25)
            logger.info(f'Removing ticket {ticket} from {environment}')
            try:
                deployment_folder = utils.ticket_deployment_folder(
                    environment, ticket, commit, True)
                source_file = Path(deployment_folder, 'deploy.py')
                SourceFileLoader('remove', str(source_file)).load_module()
            except FileNotFoundError:
                logger.error(
                    f'Cannot find deployment folder/file for ticket {ticket}')


@matador.command(name='run-sql-script')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.argument('file', type=click.File('r'))
@deploys_changes
def run_sql_script(environment, file):
    """Execute the given sql script against the database defined for the given
    environment."""
    logger.info(f'Executing {file.name} against {environment}')
    kwargs = {
        **utils.environments()[environment]['database'],
        **utils.credentials()[environment]
    }
    kwargs['directory'] = str(Path(file.name).parent)
    kwargs['file'] = file.name
    sql.run_sql_script(**kwargs)


@matador.command(name='smudge-zip')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def smudge_zip(input, output):
    input = io.open(sys.stdin.fileno(), 'rb')
    output = io.open(sys.stdout.fileno(), 'wb')
    zippey.init()
    zippey.decode(input, output)


@matador.command(name='clean-zip')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def clean_zip(input, output):
    input = io.open(sys.stdin.fileno(), 'rb')
    output = io.open(sys.stdout.fileno(), 'wb')
    zippey.init()
    zippey.encode(input, output)


@matador.command(name='start-service')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--service', '-s', prompt='Service', help='Service Label')
@windows_only
def start_service(environment, service):
    """Start the given service on the ABW Server defined for the given
    environment."""
    logger.info(f'Starting {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.start(service, services[service])


@matador.command(name='restart-service')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--service', '-s', prompt='Service', help='Service Label')
@windows_only
def restart_service(environment, service):
    """Restart the given service on the ABW Server defined for the given
    environment."""
    logger.info(f'Restarting {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.restart(service, services[service])


@matador.command(name='stop-service')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--service', '-s', prompt='Service', help='Service Label')
@windows_only
def stop_service(environment, service):
    """Stop the given service on the ABW Server defined for the given
    environment."""
    logger.info(f'Stopping {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.stop(service, services[service])


@matador.command(name='service-status')
@click.option(
    '--environment', '-e', prompt='Environment', help='Environment Name')
@click.option('--service', '-s', prompt='Service', help='Service Label')
@windows_only
def service_status(environment, service):
    """Report the status of the given service on the ABW Server defined for the
    given environment."""
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    is_running = abw_service.is_running(services[service])
    logger.info(abw_service.is_running_message(is_running, service))

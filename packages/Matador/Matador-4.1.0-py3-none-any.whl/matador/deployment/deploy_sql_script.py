import logging
from pathlib import Path

from dulwich.repo import Repo

import matador.cli.utils as utils
import matador.session as session
from matador import git
from matador.cli.sql import run_sql_script

logger = logging.getLogger(__name__)


def _fetch_script(repo, script_path, commit_ref, target_folder):
    script = Path(repo.path, script_path)
    target_script = Path(target_folder, script.name)

    git.checkout(repo, commit_ref)

    with script.open('r') as f:
        original_text = f.read()
        f.close()

    new_text = git.substitute_keywords(original_text, repo, commit_ref)

    with target_script.open('w') as f:
        f.write(new_text)
        f.close()

    return target_script


def deploy_sql_script(path, commit_ref=None):
    """Checkout an sql script from the matador repo and execute it against
    the database server defined for the environment.
    """
    script_path = Path(path)
    logger.info(f'Executing {script_path.name} against {session.environment}')
    project = Path(Repo.discover().path).name
    deployment_folder = Path(
        Path.home(), '.matador', project, session.environment, 'tickets',
        session.ticket)
    if str(script_path.parent) == '.':
        script = Path(deployment_folder, script_path)
    else:
        repo_folder = Path(Path.home(), '.matador', project, 'repository')
        repo = Repo(str(repo_folder))
        script = _fetch_script(repo, script_path, commit_ref, deployment_folder)

    kwargs = {
        **utils.environments()[session.environment]['database'],
        **utils.credentials()[session.environment]
    }
    kwargs['directory'] = str(script.parent)
    kwargs['file'] = str(script.name)

    run_sql_script(**kwargs)


def deploy_oracle_package(package_name, commit_ref=None):
    """Checkout the scripts for a package body and spec and execute them
    against the database server defined for the environment.
    """
    project = Path(Repo.discover().path).name
    deployment_folder = Path(
        Path.home(), '.matador', project, session.environment, 'tickets',
        session.ticket)
    repo_folder = Path(Path.home(), '.matador', project, 'repository')
    repo = Repo(str(repo_folder))
    package_folder = Path(
        repo_folder, 'src', 'db_objects', 'packages', package_name)
    package_spec = Path(package_folder, package_name + '.pks')
    package_body = Path(package_folder, package_name + '.pkb')

    spec_script = _fetch_script(repo, package_spec, commit_ref, deployment_folder)
    body_script = _fetch_script(repo, package_body, commit_ref, deployment_folder)

    kwargs = {
        **utils.environments()[session.environment]['database'],
        **utils.credentials()[session.environment]
    }
    kwargs['directory'] = str(spec_script.parent)
    kwargs['file'] = str(spec_script.name)

    run_sql_script(**kwargs)

    kwargs['file'] = str(body_script.name)
    run_sql_script(**kwargs)

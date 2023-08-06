#!/usr/bin/env python
import logging
from pathlib import Path
from matador.session import Session
from matador.commands.run_sql_script import run_sql_script
from matador import git


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
    if str(script_path.parent) == '.':
        script = Path(Session.deployment_folder, script_path)
    else:
        script = _fetch_script(
            Session.matador_repo, script_path, commit_ref,
            Session.deployment_folder)

    kwargs = {
        **Session.environment['database'],
        **Session.credentials
    }

    kwargs['directory'] = str(script.parent)
    kwargs['file'] = str(script.name)

    logger = logging.getLogger(__name__)
    run_sql_script(logger, **kwargs)


def deploy_oracle_package(package_name, commit_ref=None):
    """Checkout the scripts for a package body and spec and execute them
    against the database server defined for the environment.
    """
    repo_folder = Session.matador_repository_folder
    package_folder = Path(
        repo_folder, 'src', 'db_objects', 'packages', package_name)
    package_spec = Path(package_folder, package_name + '.pks')
    package_body = Path(package_folder, package_name + '.pkb')

    spec_script = _fetch_script(
        Session.matador_repo, package_spec, commit_ref,
        Session.deployment_folder)
    body_script = _fetch_script(
        Session.matador_repo, package_body, commit_ref,
        Session.deployment_folder)

    logger = logging.getLogger(__name__)
    run_sql_script(logger, spec_script)
    run_sql_script(logger, body_script)

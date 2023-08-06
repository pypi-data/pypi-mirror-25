import functools
import logging
import os
from pathlib import Path

from dulwich.repo import Repo

import matador.session as session

logger = logging.getLogger(__name__)


def windows_only(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if os.name != 'nt':
            logger.error(
                f'{func.__name__} can only be used on a Windows system')
        else:
            return func(*args, **kwargs)
    return wrapped


def deploys_changes(func):
    """Creates sub-directories in the .matador directory for the specific
    environment used by the wrapped function"""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        project = Path(Repo.discover().path).name
        environment_folder = Path(
            Path.home(), '.matador', project, kwargs['environment'])
        tickets_folder = Path(environment_folder, 'tickets')
        packages_folder = Path(environment_folder, 'packages')

        if 'ticket' in kwargs:
            session.environment = kwargs['environment']
            session.ticket = kwargs['ticket']

        Path.mkdir(environment_folder, parents=True, exist_ok=True)
        Path.mkdir(tickets_folder, parents=True, exist_ok=True)
        Path.mkdir(packages_folder, parents=True, exist_ok=True)
        return func(*args, **kwargs)
    return wrapped

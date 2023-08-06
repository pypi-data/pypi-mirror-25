import logging
import logging.config
from pathlib import Path

from dulwich.repo import Repo

from matador.cli.utils import deployment_repository


def setup(handler, verbosity):
    project_folder = Path(Repo.discover().path)
    deployment_repo = deployment_repository(project_folder)
    matador_log = Path(deployment_repo.path, 'matador.log')
    log_config = {
        'version': 1,
        'handlers': {
            'user': {
                'class': 'colorlog.StreamHandler',
                'level': verbosity.upper(),
                'formatter': handler
            },
            'matador': {
                'class': 'logging.FileHandler',
                'filename': str(matador_log),
                'level': 'INFO',
                'formatter': 'file'
            }
        },
        'formatters': {
            'console': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s%(levelname)s - %(message)s'},
            'file': {'format': (
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')}
        },
        'loggers': {
            'matador': {
                'level': 'DEBUG',
                'handlers': ['user', 'matador']
            }
        }
    }

    user_log_handlers = {
        'console': 'colorlog.StreamHandler',
        'file': 'logging.FileHandler("matador.log")'
    }
    log_config['handlers']['user']['class'] = user_log_handlers[handler]

    logging.config.dictConfig(log_config)

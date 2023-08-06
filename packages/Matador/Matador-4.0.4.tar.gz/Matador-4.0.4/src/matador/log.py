
from pathlib import Path

from dulwich.repo import Repo


def config(handler, verbosity):
    project = Path(Repo.discover().path).name
    matador_log = Path(Path.home(), '.matador', project, 'matador.log')
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

    return log_config

import win32serviceutil as win32

import matador.cli.utils as utils
import matador.session as session


def is_running(name):
    environment = utils.environments[session.environment]
    server = environment['abwServer']
    return win32.QueryServiceStatus(name, machine=server)[1] == 4


def is_running_message(is_running, label):
    if is_running:
        return f'{label} - Running on {session.environment}'
    else:
        return f'{label} - Not running on {session.environment}'


def start(label, name):
    environment = utils.environments[session.environment]
    server = environment['abwServer']
    if not is_running(name):
        win32.StartService(name, machine=server)
    message = is_running_message(is_running(name), label)
    return message


def stop(label, name):
    environment = utils.environments[session.environment]
    server = environment['abwServer']
    if is_running(name):
        win32.StopService(name, machine=server)
    message = is_running_message(is_running(name), label)
    return message


def restart(label, name):
    environment = utils.environments[session.environment]
    server = environment['abwServer']
    if is_running(name):
        win32.RestartService(name, machine=server)
    message = is_running_message(is_running(name), label)
    return message

import os
import subprocess
from collections import defaultdict
from pathlib import Path
from string import Template


def command_condition(*args):
    """

    Parameters
    ----------
    args: list
        containing boolean values for:
            if a command has been specified explicitly
            if the dbms is oracle
            if the os is posix
            if windows authentication has been specified

    Returns
    -------
        tuple of values which can be used to determine the appropriate command
        to run an sql script

    """
    try:
        most_significant_argument = args.index(True)
    except ValueError:
        most_significant_argument = -1

    conditions = {
        0: ('command'),
        1: ('oracle'),
        2: ('mssql', 'posix'),
        3: ('mssql', 'nt', 'windows_authentication'),
        -1: ('mssql', 'nt', 'mssql_authentication')
    }

    return conditions[most_significant_argument]


def command(**kwargs):
    """
    Parameters
    ----------
    kwargs : dict
        A dictionary containing values for:
            command (optional, overrides all other entries)
            dbms
            client_os
            server
            db_name
            port (Oracle only)
            windows_authentication (MSSQL on windows clients only)
            user
            password
    """
    condition = command_condition(
        'command' in kwargs,
        kwargs['dbms'].lower() == 'oracle',
        kwargs['client_os'] == 'posix',
        'windows_authentication' in kwargs)

    # Create a default dictionary based on kwargs but with any missing
    # keys returning an empty string.
    params = defaultdict(str, kwargs)

    commands = {
        ('command'):
            params['command'],
        ('oracle'):
            'sqlplus -S -L ${user}/${password}@${server}:${port}/${db_name}',
        ('mssql', 'posix'):
            'bsqldb -S ${server} -D ${db_name} -U ${user} -P ${password}',
        ('mssql', 'nt', 'windows_authentication'):
            'sqlcmd -S ${server} -d ${db_name} -E',
        ('mssql', 'nt', 'mssql_authentication'):
            'sqlcmd -S ${server} -d ${db_name} -U ${user} -P ${password}'
    }

    return Template(commands[condition]).substitute(params)


def sql_script(**kwargs):
    """
    Parameters
    ----------
    kwargs : dict
        A dictionary containing values for:
            dbms
            directory
            file
    """
    file = Path(kwargs['directory'], kwargs['file'])

    with file.open('r', encoding='utf8') as f:
        script = f.read()
        f.close()

    if kwargs['dbms'] == 'oracle':
        script += '\nshow error'

    return script.encode('utf-8')


def run_sql_script(**kwargs):
    """
    Parameters
    ----------
    kwargs : dict
        A dictionary containing values for:
            dbms
            server
            db_name
            directory
            file
    """
    kwargs['client_os'] = os.name
    cwd = os.getcwd()

    os.chdir(kwargs['directory'])

    process = subprocess.Popen(
        command(**kwargs).split(),
        stdin=subprocess.PIPE)
    process.stdin.write(sql_script(**kwargs))
    process.stdin.close()
    process.wait()

    os.chdir(cwd)

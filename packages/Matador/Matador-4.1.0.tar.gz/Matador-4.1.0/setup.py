# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

from setuptools import find_packages
from setuptools import setup

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

setup(
    name='Matador',
    version='4.1.0',
    author='Empiria Ltd',
    author_email='info@empiria.co.uk',
    entry_points={
        'console_scripts': [
            'matador = matador.cli.commands:matador',
        ],
    },
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python3',
        },
    },
    url='http://www.empiria.co.uk',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'click', 'pyyaml', 'dulwich', 'openpyxl', 'cookiecutter'],
    license='The MIT License (MIT)',
    description='Change management for Agresso systems',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ],
    python_requires='>=3.6',
)

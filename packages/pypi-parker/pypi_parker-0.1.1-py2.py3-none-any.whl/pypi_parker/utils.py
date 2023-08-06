"""Utility helpers for :class:`pypi_parker.Park`."""
import configparser
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Union

import attr

__all__ = ('generate_and_build_package', 'load_config')
FALLBACK_VALUES = dict(
    classifiers=['Development Status :: 7 - Inactive'],
    description=(
        'This package has been parked either for future use or to protect against typo misdirection.'
        ' If you believe that it has been parked in error, please contact the package owner.'
    )
)
LIST_LITERAL_KEYS = ('classifiers',)
ALLOWED_SETUP_SUFFIXES = ('sdist', 'check -r -s')
SETUP_CONFIG = Dict[str, Union[str, List[str]]]


@attr.s
class SpecificTemporaryFile(object):
    """Context manager for temporary files with a known desired name and body."""

    name = attr.ib(validator=attr.validators.instance_of(str))
    body = attr.ib(validator=attr.validators.instance_of(str))

    def _write_file(self) -> None:
        """Write the requested body to the requested file."""
        with open(self.name, 'w') as file:
            file.write(self.body)

    def _delete_file(self) -> None:
        """Delete the created file."""
        os.remove(self.name)

    def __enter__(self) -> object:
        """Create the specified file and write the body on enter."""
        self._write_file()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Clean up the created file."""
        self._delete_file()


def _string_literal_to_lines(string_literal: str) -> List[str]:
    """Split a string literal into lines.

    :param str string_literal: Source to split
    :rtype: list of str
    """
    return [
        line.strip() for line
        in string_literal.split()
    ]


def _generate_setup(config: configparser.ConfigParser, name: str) -> SETUP_CONFIG:
    """Generate a ``setuptools.setup`` call for ``name`` from ``config``.

    :param config: Loaded parker config
    :type config: configparser.ConfigParser
    :param str name:
    """
    setup_base = {}  # type: SETUP_CONFIG
    if name in config:
        setup_base.update(dict(config[name].items()))
    else:
        setup_base.update(dict(config['DEFAULT'].items()))
    setup_base['name'] = name

    if name in config:
        setup_base.update(config[name].items())

    try:
        description_keys = _string_literal_to_lines(setup_base.pop('description_keys'))
        description_setup = {key: str(setup_base[key]) for key in description_keys}  # type: Dict[str, str]
        setup_base['description'] = str(setup_base['description']).format(**description_setup)
    except KeyError:
        pass

    for key in LIST_LITERAL_KEYS:
        try:
            setup_base[key] = _string_literal_to_lines(str(setup_base[key]))
        except KeyError:
            pass

    for key, value in FALLBACK_VALUES.items():
        if key not in setup_base:
            setup_base[key] = value

    if 'long_description' not in setup_base:
        setup_base['long_description'] = setup_base['description']

    return setup_base


def load_config(filename: str) -> List[SETUP_CONFIG]:
    """Load ``parker.conf`` and generate all ``setuptools.setup`` calls."""
    config = configparser.ConfigParser()
    config.read(filename)

    names = config.sections()
    if 'names' in config:
        names.remove('names')
        names.extend([
            name for name in config['names']
            if name not in names and name not in config['DEFAULT']
        ])

    for name in names:
        yield _generate_setup(config, name)


def _setup_body(setup_conf: SETUP_CONFIG) -> str:
    """Generate the setup.py body given a setup config.

    .. note::

        The setup.py generated here will raise an ImportError for every actions
        except for those whitelisted for use when building the package.

    :param dict setup_conf: Setup config for which to generate setup.py
    :rtype: str
    """
    return os.linesep.join([
        'import sys',
        'from setuptools import setup',
        '',
        "args = ' '.join(sys.argv[1:]).strip()",
        'if not args in ({allowed_suffixes}):',
        '    raise {error}',
        '',
        'setup(',
        '    {config}',
        ')',
        ''
    ]).format(
        error=repr(ImportError(setup_conf['description'])),
        config=',\n    '.join([
            '{}= {}'.format(key, repr(value))
            for key, value
            in setup_conf.items()
        ]),
        allowed_suffixes=', '.join(repr(each) for each in ALLOWED_SETUP_SUFFIXES)
    )


def generate_and_build_package(package_config: SETUP_CONFIG, origin_directory: str) -> None:
    """Generates, validates, and builds a package using the specified configuration and places
    the resulting distributable files in ``{origin_directory}/dist``.

    :param dist package_config: Package setup configuration
    :param str origin_directory: Filepath to desired base output directory
    """

    with tempfile.TemporaryDirectory() as tmpdirname:

        os.chdir(tmpdirname)

        setup_py = SpecificTemporaryFile(
            name=os.path.join(tmpdirname, 'setup.py'),
            body=_setup_body(package_config)
        )

        manifest_in = SpecificTemporaryFile(
            name=os.path.join(tmpdirname, 'MANIFEST.in'),
            body='include setup.py'
        )

        with setup_py, manifest_in:
            validate_command = [sys.executable, setup_py.name, 'check', '-r', '-s']
            subprocess.check_call(validate_command)

            build_command = [sys.executable, setup_py.name, 'sdist']
            subprocess.check_call(build_command)

        for file in glob.glob(os.path.join(tmpdirname, 'dist/*')):
            shutil.copy(file, os.path.join(origin_directory, 'dist'))

        os.chdir(origin_directory)

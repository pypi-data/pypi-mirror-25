# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Carmen Bianca Bakker <carmen@carmenbianca.eu>
#
# This file is part of changelogdir.
#
# changelogdir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# changelogdir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with changelogdir.  If not, see <http://www.gnu.org/licenses/>.

"""Generate a changelog from a directory structure to avoid merge conflicts."""

import argparse
import configparser
import json
import pathlib
import sys
from collections import defaultdict

__author__ = 'Carmen Bianca Bakker <carmen@carmenbianca.eu>'
__all__ = []
__version__ = '3.1.0'

# pylint: disable=too-few-public-methods,missing-docstring,redefined-outer-name


class _Path:

    def __init__(self, path):
        self.path = pathlib.Path(path)

    def __lt__(self, other):
        return self.path < other.path

    def __repr__(self):
        return repr(self.path)


class Section(_Path):

    def __init__(self, path):
        super().__init__(path)
        self.subsections = []
        self.variables = []
        self.entries = []


def filter_name(name):
    """The gist of this function: Turn '001_hello' into 'hello'.

    Basically, remove the stuff before the first underscore, including the
    underscore itself.
    """
    if '_' in name:
        return name.split('_', 1)[1]
    return name


def default_config():
    """Generate a default config object.

    :return: Configuration.
    :rtype: :class:`ConfigParser`
    """
    defaults = {
        'directory': 'CHANGELOG',
        'file_extension': 'md',
        'reversed_sections': '[2]',
        'h1': '# Changelog',
        'h2': '## {name}',
        'h3': '### {name}',
    }
    config = configparser.ConfigParser()
    config.read_dict({'changelogdir': defaults})
    return config


def parse_config(config, config_file):
    """Parse *config_file* and write it into *config*."""
    config.read_file(config_file)


def changelog_tree(section, file_extension):
    """Build a tree on top of *section*.

    Find all subsections, variables and entries inside of *section* and add
    them to its attributes.

    For every subsection, (recursively) do the same.
    """
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension
    if not section.path.is_dir():
        raise ValueError('{} is not a directory'.format(repr(section.path)))

    files = list(section.path.iterdir())
    section.subsections = sorted(Section(subsection)
                                 for subsection in files
                                 if subsection.is_dir())
    section.variables = sorted(pathlib.Path(variable)
                               for variable in files
                               if variable.is_file()
                               and variable.name.startswith('_'))
    section.entries = sorted(pathlib.Path(entry)
                             for entry in files
                             if entry.is_file()
                             and entry.suffix == file_extension)
    for subsection in section.subsections:
        changelog_tree(subsection, file_extension)


def render(section, write_func, config, level=1):
    """Render *section* recursively with *write_func*.

    All sections have the 'name' variable defaulted to their filtered
    filename.

    Missing variables default to empty string.
    """
    reversed_sections = json.loads(config['reversed_sections'])

    variables = defaultdict(str)

    for variable in section.variables:
        with variable.open() as fp:
            contents = fp.read().strip('\n')
        # if variable.name is '_date', then variables['date'] = contents
        variables[variable.name[1:]] = contents

    variables.setdefault('name', filter_name(section.path.name))

    header_string = config['h{}'.format(level)]
    header = header_string.format_map(variables)

    write_func(header)
    write_func('\n')

    for entry in section.entries:
        write_func('\n')
        with entry.open() as fp:
            contents = fp.read()
        write_func(contents)

    if level + 1 in reversed_sections:
        subsections = list(reversed(section.subsections))
    else:
        subsections = section.subsections

    for subsection in subsections:
        write_func('\n')
        render(subsection, write_func, config, level + 1)


def find_config_file(directory):
    """Find config file in directory.

    If none is found, return None.
    """
    path = pathlib.Path(directory)

    files = list(path.iterdir())

    # The first file that matches is our configuration file.
    priorities = [
        '.changelogdirrc',
        'changelogdirrc',
        'setup.cfg',
    ]

    for target in priorities:
        if target in map(lambda file_: file_.name, files):
            return directory / pathlib.Path(target)
    return None


def main(argv=None):  # pylint: disable=too-many-branches
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Generate a changelog from a directory structure.',
        epilog='If no output file is specified, write to STDOUT.')
    parser.add_argument('-o', '--output', help='File to write to')
    parser.add_argument('-c', '--config',
                        help='Path to config file')
    parser.add_argument('-d', '--directory',
                        help='Override path to changelog directory')
    parsed = parser.parse_args(argv)

    config = default_config()

    if parsed.config:
        config_path = pathlib.Path(parsed.config)
    else:
        config_path = find_config_file('.')


    if config_path is not None:
        try:
            with config_path.open() as fp:
                parse_config(config, fp)
        except (IOError, configparser.Error):
            raise
        config_directory = config_path.resolve().parent
    else:
        config_directory = pathlib.Path('.')

    config = config['changelogdir']

    directory = (pathlib.Path(parsed.directory)
                 if parsed.directory else
                 config_directory / pathlib.Path(config['directory']))

    section = Section(directory)
    changelog_tree(section, config['file_extension'])

    # If output file was specified, write to that file.  Else, write to STDOUT.
    if parsed.output:
        with open(parsed.output, 'w') as output_file:
            render(section, output_file.write, config)
    else:
        render(section, sys.stdout.write, config)


if __name__ == '__main__':
    main()

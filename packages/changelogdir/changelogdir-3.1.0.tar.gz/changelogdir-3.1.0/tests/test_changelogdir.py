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

"""Tests for changelogdir._config."""

import configparser
import io
from os import path

import pytest

import changelogdir

TESTS_DIRECTORY = path.dirname(path.abspath(__file__))
PROJECT_DIRECTORY = path.join(TESTS_DIRECTORY, 'demo-project')
CHANGELOG_DIRECTORY = path.join(PROJECT_DIRECTORY, 'CHANGELOG')


def test_parse_config_wrong_format():
    """:func:`parse_config` throws a configparser.Error when the file format is
    invalid.
    """
    fake_file = io.StringIO('{"name": "value"}')
    config = configparser.ConfigParser()
    with pytest.raises(configparser.Error):
        changelogdir.parse_config(config, fake_file)


def test_filter_name():
    """:func:`filter_name` removes everything up to and including the first
    underscore.
    """
    name = '000_hello'
    result = changelogdir.filter_name(name)
    assert result == 'hello'


def test_filter_name_only_first_underscore():
    """:func:`filter_name` does not remove the second underscore. """
    name = '000_hello_world'
    result = changelogdir.filter_name(name)
    assert result == 'hello_world'


def test_filter_name_no_underscore():
    """:func:`filter_name` doesn't do anything when there is no underscore."""
    name = 'hello'
    assert changelogdir.filter_name(name) == name


def test_changelog_tree():
    """:func:`changelog_tree` creates a correct tree."""
    root_section = changelogdir.Section(CHANGELOG_DIRECTORY)
    changelogdir.changelog_tree(root_section, 'rst')
    # Very very hardcoded.  But it's good enough
    assert len(root_section.subsections) == 3
    assert root_section.subsections == sorted(root_section.subsections)
    unreleased = root_section.subsections[2]
    assert len(unreleased.entries) == 3
    assert len(unreleased.subsections) == 0
    assert len(unreleased.variables) == 1
    v1 = root_section.subsections[0]
    assert len(v1.entries) == 1
    assert len(v1.subsections) == 3
    assert len(v1.variables) == 1
    assert unreleased.subsections == sorted(unreleased.subsections)
    security = v1.subsections[0]
    assert len(security.entries) == 1
    assert len(security.subsections) == 0
    assert len(security.variables) == 0


def test_changelog_tree_wrong_extension():
    """:func:`changelog_tree` does not return entries if the wrong file
    extension is given.
    """
    root_section = changelogdir.Section(CHANGELOG_DIRECTORY)
    changelogdir.changelog_tree(root_section, 'md')
    unreleased = root_section.subsections[0]
    assert len(unreleased.entries) == 0


def test_changelog_tree_not_exists(tmpdir):
    """:func:`changelog_tree` throws a ValueError when the provided directory
    does not exist or is not a directory.
    """
    directory = tmpdir.mkdir('tmp').join('not-exist')
    directory = str(directory)
    root_section = changelogdir.Section(directory)
    with pytest.raises(ValueError):
        changelogdir.changelog_tree(root_section, 'extension')


def test_render():
    """:func:`render` correctly renders our little demo project."""
    fake_file = io.StringIO()
    write_func = fake_file.write
    config = changelogdir.default_config()
    with open(path.join(PROJECT_DIRECTORY, '.changelogdirrc')) as fp:
        changelogdir.parse_config(config, fp)
    config = config['changelogdir']
    section = changelogdir.Section(CHANGELOG_DIRECTORY)
    changelogdir.changelog_tree(section, 'rst')
    changelogdir.render(
        section,
        write_func,
        config
    )

    with open(path.join(PROJECT_DIRECTORY, 'expected.rst')) as fp:
        expected = fp.read()

    assert expected == fake_file.getvalue()

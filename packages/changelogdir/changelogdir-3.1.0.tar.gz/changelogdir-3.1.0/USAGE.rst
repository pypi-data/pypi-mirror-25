Usage
=====

Command line invocation
-----------------------

.. literalinclude:: help.txt

Typically, you do not need to specify any arguments.

::

  changelogdir > CHANGELOG.md

is equal to::

  changelogdir -c .changelogdirrc -d CHANGELOG -o CHANGELOG.md

Directory structure
-------------------

The directory structure of your project might look somewhat like this:

.. literalinclude:: tree.txt

You can find this directory structure at
https://gitlab.com/carmenbianca/changelogdir/tree/master/tests/demo-project.

For clarity's sake, we will describe this structure with the following glossary:

- *Project root* - The very root of your project.  This contains your
  changelog directory and changelog file.

- *Configuration file* - The ``.changelogdirrc`` file.  See `Configuration`_.

- *Changelog directory* - The ``CHANGELOG`` directory.

- *Section* - All directories (and subdirectories, and subsubdirectories)
  underneath the changelog directory.

  - The sections at the root level are typically releases (X.Y.Z,
    zzz_Unreleased).

  - The subsections can be named as suggested by `Keep a Changelog
    <http://keepachangelog.com>`_:

    - "Added" for new features.

    - "Changed" for changes in existing functionality.

    - "Deprecated" for once-stable features removed in upcoming releases.

    - "Removed" for deprecated features removed in this release.

    - "Fixed" for any bug fixes.

    - "Security" to invite users to upgrade in case of vulnerabilities.

  - Or just use the sections however you like.

- *Entry* - All files with your specified file extension belonging to a section.

- *Variable file* - Any file starting with a ``_`` (and without file extension).
  The purpose of these files is described in `h{1..∞}`_.

The above structure renders to:

.. literalinclude:: expected.rst
  :language: restructuredtext

All sections and entries are padded by one empty line above them.

Ordering
~~~~~~~~

The sections and entries are ordered alphabetically by their file and directory
names:

- You can add "XXX\_" before your file or directory name to influence the order
  in which they appear.  "XXX\_" itself is not shown in the rendered changelog.
  See `h{1..∞}`_.

- Sections and entries are in *ascending* order.  This is the expected behaviour
  by most users.  The section "Added" appears before "Deprecated", and section
  "000_Security" appears before "Added".

- *However*, top-level sections are in *descending* order.  This isn't very
  intuitive until you realise that this causes the *highest*/*newest* sections
  to appear at the top.  Typically, you might name your "Unreleased" section
  "zzz_Unreleased" to make sure that it is always on top.

- The alphabetical order of sections can be configured in `reversed_sections`_.

Configuration
-------------

The configuration file is optional.  If no configuration file is found or
specified, it defaults to::

  [changelogdir]
  directory = CHANGELOG
  file_extension = md
  reversed_sections = [2]
  h1 = # Changelog
  h2 = ## {name}
  h3 = ### {name}

When adding a configuration file, you only have to specify the keys that you
want to change from their defaults.

changelogdir searches for a configuration file in the current directory in the
following order and uses the first one it finds:

- ``.changelogdirrc``

- ``changelogdirrc``

- ``setup.cfg``

directory
~~~~~~~~~

Directory relative to the configuration file that contains the changelog
structure.

file_extension
~~~~~~~~~~~~~~

The extension used by entry files.

reversed_sections
~~~~~~~~~~~~~~~~~

All sections listed here are rendered in reverse alphabetical order.  The syntax
is equal to a Python list.  ``[]`` is an empty list.  ``[2, 3]`` is a list of
two items.

h{1..∞}
~~~~~~~

A string of text that is put at the very top of the output.  This string can
span multiple lines::

  h1 = =========
       Changelog
       =========
  # or a different indentation:
  h1 = =========
    Changelog
    =========

The indentation level is irrelevant and will be stripped from the output.  Just
be consistent.  Thus, both above examples will become::

  =========
  Changelog
  =========

The number after the 'h' indicates the level.  "h1" is the absolute top header.
"h2" is the header of all top-level sections.  "h3" is the header of subsections
of "h2".  And so forth.  You can go as deep as you want.

You can also use variables inside of your headers::

  h2 = ## {name} - {date}

These variables are unique per section, and are defined in ``_variable`` files
inside of the section directories.  So, given a tree like this::

  CHANGELOG
  └── zzz_Unreleased
      ├── _date
      └── entry.md

``{date}`` will be equal to the contents of the ``_date`` file.

You can define any variables that you like.  Probably.  It likely won't accept
some special characters.  Just be sensible.

If a variable is defined in a section header but no corresponding file can be
found, then the variable will default to an empty string.

``{name}`` is unique, however, and is equal to the directory name of the section
*after* the first underscore.  So, if you have a directory named
"zzz_Unreleased", ``{name}`` is equal to "Unreleased".  But if you want, you can
override this with a ``_name`` file.

See `Ordering`_ for an explanation on the ``zzz_`` prefix.

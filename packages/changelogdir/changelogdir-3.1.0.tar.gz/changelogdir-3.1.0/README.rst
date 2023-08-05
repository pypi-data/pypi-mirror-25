changelogdir
============

Generate a changelog from a directory structure to avoid merge conflicts.

- Free software: GPLv3+

- Documentation: https://carmenbianca.gitlab.io/changelogdir

- Source code: https://gitlab.com/carmenbianca/changelogdir

- PyPI: https://pypi.python.org/pypi/changelogdir

- Python: 3.4+

- Author: Carmen Bianca Bakker  <carmen@carmenbianca.eu>

changelogdir is a simple utility that allows you to turn a directory structure
into a changelog file.  Every feature/bugfix/whatever gets its own file to list
changes in, thereby avoiding merge conflict crises such as described `here
<https://gitlab.com/gitlab-org/gitlab-ce/issues/17826>`_.

changelogdir is partially inspired by
`Keep a Changelog <http://keepachangelog.com>`_.

A simple example
----------------

Say we have a ``CHANGELOG.md`` in our master branch that looks like this::

  # Changelog

  ## 1.0.0

  - Added support for TempleOS.

And Developer A comes along and does the following in their branch::

  # Changelog

  ## 1.0.0

  - Added support for TempleOS.

  - Deprecated support for Windows.

And Developer B has this in their branch::

  # Changelog

  ## 1.0.0

  - Added support for TempleOS.

  - Added support for Android.

Then merging the two branches into master causes a merge conflict, and it's just
a needless headache.

changelogdir fixes this by putting those entries into individual files.  Thus,
you'd end up with something looking like this::

  awesome-project
  ├── CHANGELOG
  │   └── 1.0.0
  │       ├── android.md
  │       ├── templeos.md
  │       └── windows.md
  └── .changelogdirrc

``.changelogdirrc`` contains::

  [changelogdir]
  directory = CHANGELOG
  file_extension = md
  h1 = # Changelog
  h2 = ## {name}

``android.md`` contains::

  - Added support for Android.

``templeos.md`` contains::

  - Added support for TempleOS.

``windows.md`` contains::

  - Deprecated support for Windows.

And when running ``changelogdir``, the following is generated in alphabetical
order of the file names::

  ~/awesome-project$ changelogdir
  # Changelog

  ## 1.0.0

  - Added support for Android.

  - Added support for TempleOS.

  - Deprecated support for Windows.

Of course, it might make more sense to put those three changes into a single
file called ``platform-changes.md``, but this is merely for demonstration.

Installation
------------

See :doc:`INSTALLATION`.

Usage
-----

See :doc:`USAGE`.

Why doesn't changelogdir have its changelog in the Python package?
------------------------------------------------------------------

Doing this would require having changelogdir installed to be able to build
itself.  There is probably a way around this (just call changelogdir.py
directly), but it'd be really ugly.

As a compromise, it does generate its own changelog when creating and uploading
the docs.  See :doc:`CHANGELOG`.

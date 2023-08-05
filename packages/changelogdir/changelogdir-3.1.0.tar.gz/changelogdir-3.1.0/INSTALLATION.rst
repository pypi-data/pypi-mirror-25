Installation
============

changelogdir requires Python 3.4 or higher.  There are no other requirements,
though pip/setuptools makes installation a lot easier.

Using pip
---------

The easiest way to install changelogdir is by using pip.  This downloads the
latest version of changelogdir from PyPI and installs it as a Python package.
In one simple step::

    pip3 install changelogdir

The caveat is that the above command may complain about requiring root
permissions.  It is *not advisable* to grant pip those permissions.  You'll end
up with files on your filesystem that are not managed by your package manager.
Instead, tell pip to install the package as your local user::

    pip3 install --user changelogdir

This installs ``changelogdir`` into ``~/.local/bin``.  You only need to add that
folder to your ``PATH`` by adding a line like this to your ``.bashrc``::

    export PATH="$HOME/.local/bin:$PATH"

Without pip
-----------

Suppose you don't want to use pip, then you can simply drop ``changelogdir.py``
into your project directory.  You can download it from `here
<https://gitlab.com/carmenbianca/changelogdir/raw/master/src/changelogdir.py>`_.

Then, instead of calling ``changelogdir``, you would call ``python3
changelog.py`` inside of your project directory.

Usage
-----

After you've installed changelogdir, see :doc:`Usage <USAGE>` to get started.

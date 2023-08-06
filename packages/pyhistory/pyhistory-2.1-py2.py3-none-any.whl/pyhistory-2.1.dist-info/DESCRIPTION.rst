==============
Python History
==============

.. image:: https://badge.fury.io/py/pyhistory.png
    :target: http://badge.fury.io/py/pyhistory

.. image:: https://travis-ci.org/beregond/pyhistory.png?branch=master
        :target: https://travis-ci.org/beregond/pyhistory

.. image:: https://img.shields.io/pypi/dm/pyhistory.svg
        :target: https://pypi.python.org/pypi/pyhistory

.. image:: https://coveralls.io/repos/beregond/pyhistory/badge.png
    :target: https://coveralls.io/r/beregond/pyhistory


App to maintain history file for your project.

* Free software: BSD license
* Source: https://github.com/beregond/pyhistory
* PyPI: https://pypi.python.org/pypi/pyhistory

PyHistory
---------

PyHistory maintains history entries in distributed work environment, which
allows many developers to add/remove history entries between releases without
conflicts.

Installation
------------

.. code-block:: bash

  pip install pyhistory

Features
--------

(All commands can start either with `pyhistory` or shortcut - `pyhi`.)

* Add history entry:

  .. code-block:: bash

    $ pyhi add 'New feature'
    $ pyhi add Something

* List history entries:

  .. code-block:: bash

    $ pyhi list

    * New feature
    * Something

* Update your history file with entries for given release:

  .. code-block:: bash

    $ cat HISTORY.rst
    my project
    ==========

    0.4.1 (2015-08-04)
    ++++++++++++++++++

    * Added PyHistory to project.
    * Improved codebase.
    * Other features.

    $ pyhi update 0.4.2
    $ cat HISTORY.rst
    my project
    ==========

    0.4.2 (2015-08-05)
    ++++++++++++++++++

    * Bug fixes
    * Change in API
    * Removed old features

    0.4.1 (2015-08-04)
    ++++++++++++++++++

    * Added PyHistory to project
    * Improved codebase
    * Other features

* Delete selected entries:

  .. code-block:: bash

    $ pyhi delete

    1. New feature
    2. Something
    3. Another one
    4. Wrong one

    (Delete by choosing entries numbers.)

    $ pyhi delete 2 4
    $ pyhi list

    * New feature
    * Another one

* Clear all history:

  .. code-block:: bash

    $ pyhi clear
    Do you really want to remove all entries? [y/N]: y

  Or without prompt:

  .. code-block:: bash

    $ pyhi clear --yes

Config file
-----------

You can adjust Pyhistory behaviour to your needs by ``setup.cfg`` file. Just
put ``pyhistory`` section in there:

.. code-block:: ini

  [pyhistory]
  history_dir = some_dir  # 'history' by default
  history_file = myhistory.rst  # 'HISTORY.rst' by default
  at_line = 42  # by default history will be injected after first headline




History
-------

2.1 (2017-09-29)
++++++++++++++++

* Fixed error for empty file.
* Unpinned hard requirements for package.
* Added support for py35 and py36.

2.0 (2015-08-07)
++++++++++++++++

* Added line splitting.
* Moved CLI interface to Click library.
* Added '--yes' flag for clear command.
* Removed 'squash' subcommand.
* Added microseconds to generated files.
* 0 as at-line option in no longer valid.

1.3 (2014-10-17)
++++++++++++++++

* Timestamps are now in miliseconds (again).
* Added load config from file.

1.2.1 (2014-08-06)
++++++++++++++++++

* Improved format of generated hash (no miliseconds now).

1.2 (2014-07-22)
++++++++++++++++

* Added delete command.

1.1 (2014-07-15)
++++++++++++++++

* Added timestamp to generated files, so now entries are properly ordered.
* Pyhistory traverses directory tree to find proper place for history directory.

1.0.3 (2014-06-23)
++++++++++++++++++

* Added squash command (alias to update).

1.0.2 (2014-06-22)
++++++++++++++++++

* Further bug fixing of start detecting.

1.0.1 (2014-06-20)
++++++++++++++++++

* Fixed error raised by `clear` when history dir is absent.
* Fixed `update` - command will now try to find file start.

1.0 (2014-06-20)
++++++++++++++++

* First release on PyPI.



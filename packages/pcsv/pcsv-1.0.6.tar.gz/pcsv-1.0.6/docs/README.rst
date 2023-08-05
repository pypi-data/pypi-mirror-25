.. README.rst
.. Copyright (c) 2013-2017 Pablo Acosta-Serafini
.. See LICENSE for details


.. image:: https://badge.fury.io/py/pcsv.svg
    :target: https://pypi.python.org/pypi/pcsv
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/pcsv.svg
    :target: https://pypi.python.org/pypi/pcsv
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/pcsv.svg
    :target: https://pypi.python.org/pypi/pcsv
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/pcsv.svg
    :target: https://pypi.python.org/pypi/pcsv
    :alt: Format

|

.. image::
   https://travis-ci.org/pmacosta/pcsv.svg?branch=master

.. image::
   https://ci.appveyor.com/api/projects/status/
   7dpk342kxs8kcg5t/branch/master?svg=true
   :alt: Windows continuous integration

.. image::
   https://codecov.io/github/pmacosta/pcsv/coverage.svg?branch=master
   :target: https://codecov.io/github/pmacosta/pcsv?branch=master
   :alt: Continuous integration coverage

.. image::
   https://readthedocs.org/projects/pip/badge/?version=stable
   :target: http://pip.readthedocs.org/en/stable/?badge=stable
   :alt: Documentation status

|

Description
===========

.. role:: bash(code)
        :language: bash

.. [[[cog
.. import os, sys
.. from docs.support.term_echo import ste
.. file_name = sys.modules['docs.support.term_echo'].__file__
.. mdir = os.path.realpath(
..     os.path.dirname(os.path.dirname(os.path.dirname(file_name)))
.. )
.. import docs.support.requirements_to_rst
.. docs.support.requirements_to_rst.def_links(cog)
.. ]]]
.. _Astroid: https://bitbucket.org/logilab/astroid
.. _Cog: http://nedbatchelder.com/code/cog
.. _Coverage: http://coverage.readthedocs.org/en/coverage-4.0a5
.. _Docutils: http://docutils.sourceforge.net/docs
.. _Mock: http://www.voidspace.org.uk/python/mock
.. _Pexdoc: http://pexdoc.readthedocs.org
.. _Pmisc: http://pmisc.readthedocs.org
.. _PyContracts: https://andreacensi.github.io/contracts
.. _Pylint: http://www.pylint.org
.. _Py.test: http://pytest.org
.. _Pytest-coverage: https://pypi.python.org/pypi/pytest-cov
.. _Pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _Sphinx: http://sphinx-doc.org
.. _ReadTheDocs Sphinx theme: https://github.com/snide/sphinx_rtd_theme
.. _Inline Syntax Highlight Sphinx Extension:
   https://bitbucket.org/klorenz/sphinxcontrib-inlinesyntaxhighlight
.. _Tox: https://testrun.org/tox
.. _Virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs
.. [[[end]]]

This module can be used to handle comma-separated values (CSV) files and do
lightweight processing of their data with support for row and column
filtering. In addition to basic read, write and data replacement, files
can be concatenated, merged, and sorted

Examples
--------

Read/write
^^^^^^^^^^

.. literalinclude:: ./support/pcsv_example_1.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

Replace data
^^^^^^^^^^^^

.. literalinclude:: ./support/pcsv_example_2.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

Concatenate two files
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ./support/pcsv_example_3.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

Merge two files
^^^^^^^^^^^^^^^

.. literalinclude:: ./support/pcsv_example_4.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

Sort a file
^^^^^^^^^^^

.. literalinclude:: ./support/pcsv_example_5.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

Interpreter
===========

The package has been developed and tested with Python 2.6, 2.7, 3.3, 3.4,
3.5 and 3.6 under Linux (Debian, Ubuntu), Apple macOS and Microsoft Windows

Installing
==========

.. code-block:: bash

        $ pip install pcsv

Documentation
=============

Available at `Read the Docs <https://pcsv.readthedocs.org>`_

Contributing
============

1. Abide by the adopted `code of conduct
   <http://contributor-covenant.org/version/1/3/0>`_

2. Fork the `repository <https://github.com/pmacosta/pcsv>`_ from
   GitHub and then clone personal copy [#f1]_:

        .. code-block:: bash

                $ git clone \
                      https://github.com/[github-user-name]/pcsv.git
                Cloning into 'pcsv'...
                ...
                $ cd pcsv
                $ export PCSV_DIR=${PWD}

3. Install the project's Git hooks and build the documentation. The pre-commit
   hook does some minor consistency checks, namely trailing whitespace and
   `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ compliance via
   Pylint. Assuming the directory to which the repository was cloned is
   in the :bash:`$PCSV_DIR` shell environment variable:

        .. code-block:: bash

                $ ${PCSV_DIR}/sbin/complete-cloning.sh
                Installing Git hooks
                Building pcsv package documentation
                ...

4. Ensure that the Python interpreter can find the package modules
   (update the :bash:`$PYTHONPATH` environment variable, or use
   `sys.paths() <https://docs.python.org/2/library/sys.html#sys.path>`_,
   etc.)

        .. code-block:: bash

                $ export PYTHONPATH=${PYTHONPATH}:${PCSV_DIR}

5. Install the dependencies (if needed, done automatically by pip):

    .. [[[cog
    .. import docs.support.requirements_to_rst
    .. docs.support.requirements_to_rst.proc_requirements(cog)
    .. ]]]


    * `Astroid`_ (Python 2.6: older than 1.4, Python 2.7 or newer: 1.3.8
      or newer)

    * `Cog`_ (2.4 or newer)

    * `Coverage`_ (3.7.1 or newer)

    * `Docutils`_ (Python 2.6: 0.12 or newer and older than 0.13, Python
      2.7: 0.12 or newer, Python 3.3: 0.12 or newer and older than 0.13,
      Python 3.4: 0.12 or newer, Python 3.5: 0.12 or newer, Python 3.6:
      0.12 or newer)

    * `Inline Syntax Highlight Sphinx Extension`_ (0.2 or newer)

    * `Mock`_ (Python 2.x only, 1.0.1 or newer)

    * `Pexdoc`_ (1.0.9 or newer)

    * `Pmisc`_ (1.2.2 or newer)

    * `Py.test`_ (2.7.0 or newer)

    * `PyContracts`_ (1.7.2 or newer except 1.7.7)

    * `Pylint`_ (Python 2.6: 1.3 or newer and older than 1.4, Python 2.7
      or newer: 1.3.1 or newer)

    * `Pytest-coverage`_ (1.8.0 or newer)

    * `Pytest-xdist`_ (optional, 1.8.0 or newer)

    * `ReadTheDocs Sphinx theme`_ (0.1.9 or newer)

    * `Sphinx`_ (Python 2.6: 1.2.3 or newer and 1.4.9 or older, Python
      2.7: 1.5 or newer, Python 3.3: 1.2.3 or newer and 1.4.9 or older,
      Python 3.4: 1.5 or newer, Python 3.5: 1.5 or newer, Python 3.6:
      1.5 or newer)

    * `Tox`_ (1.9.0 or newer)

    * `Virtualenv`_ (13.1.2 or newer)

    .. [[[end]]]

6. Implement a new feature or fix a bug

7. Write a unit test which shows that the contributed code works as expected.
   Run the package tests to ensure that the bug fix or new feature does not
   have adverse side effects. If possible achieve 100% code and branch
   coverage of the contribution. Thorough package validation
   can be done via Tox and Py.test:

        .. code-block:: bash

            $ tox
            GLOB sdist-make: .../pcsv/setup.py
            py26-pkg inst-nodeps: .../pcsv/.tox/dist/pcsv-...zip

   `Setuptools <https://bitbucket.org/pypa/setuptools>`_ can also be used
   (Tox is configured as its virtual environment manager) [#f2]_:

        .. code-block:: bash

            $ python setup.py tests
            running tests
            running egg_info
            writing requirements to pcsv.egg-info/requires.txt
            writing pcsv.egg-info/PKG-INFO
            ...

   Tox (or Setuptools via Tox) runs with the following default environments:
   ``py26-pkg``, ``py27-pkg``, ``py33-pkg``, ``py34-pkg`` and ``py35-pkg``
   [#f3]_. These use the Python 2.6, 2.7, 3.3, 3.4 and 3.5 interpreters,
   respectively, to test all code in the documentation (both in Sphinx
   ``*.rst`` source files and in docstrings), run all unit tests, measure test
   coverage and re-build the exceptions documentation. To pass arguments to
   Py.test (the test runner) use a double dash (``--``) after all the Tox
   arguments, for example:

        .. code-block:: bash

            $ tox -e py27-pkg -- -n 4
            GLOB sdist-make: .../pcsv/setup.py
            py27-pkg inst-nodeps: .../pcsv/.tox/dist/pcsv-...zip
            ...

   Or use the :code:`-a` Setuptools optional argument followed by a quoted
   string with the arguments for Py.test. For example:

        .. code-block:: bash

            $ python setup.py tests -a "-e py27-pkg -- -n 4"
            running tests
            ...

   There are other convenience environments defined for Tox [#f4]_:

    * ``py26-repl``, ``py27-repl``, ``py33-repl``, ``py34-repl`` and
      ``py35-repl`` run the Python 2.6, 2.7, 3.3, 3.4 or 3.5 REPL,
      respectively, in the appropriate virtual environment. The ``pcsv``
      package is pip-installed by Tox when the environments are created.
      Arguments to the interpreter can be passed in the command line
      after a double dash (``--``)

    * ``py26-test``, ``py27-test``, ``py33-test``, ``py34-test`` and
      ``py35-test`` run py.test using the Python 2.6, 2.7, 3.3, 3.4
      or Python 3.5 interpreter, respectively, in the appropriate virtual
      environment. Arguments to py.test can be passed in the command line
      after a double dash (``--``) , for example:

        .. code-block:: bash

            $ tox -e py34-test -- -x test_eng.py
            GLOB sdist-make: [...]/pcsv/setup.py
            py34-test inst-nodeps: [...]/pcsv/.tox/dist/pcsv-[...].zip
            py34-test runtests: PYTHONHASHSEED='680528711'
            py34-test runtests: commands[0] | [...]py.test -x test_eng.py
            ==================== test session starts ====================
            platform linux -- Python 3.4.2 -- py-1.4.30 -- [...]
            ...

    * ``py26-cov``, ``py27-cov``, ``py33-cov``, ``py34-cov`` and
      ``py35-cov`` test code and branch coverage using the Python 2.6,
      2.7, 3.3, 3.4 or 3.5 interpreter, respectively, in the appropriate
      virtual environment. Arguments to py.test can be passed in the command
      line after a double dash (``--``). The report can be found in
      :bash:`${PCSV_DIR}/.tox/py[PV]/usr/share/pcsv/tests/htmlcov/index.html`
      where ``[PV]`` stands for ``26``, ``27``, ``33``, ``34`` or ``35``
      depending on the interpreter used

8. Verify that continuous integration tests pass. The package has continuous
   integration configured for Linux (via `Travis <http://www.travis-ci.org>`_)
   and for Microsoft Windows (via `Appveyor <http://www.appveyor.com>`_).
   Aggregation/cloud code coverage is configured via
   `Codecov <https://codecov.io>`_. It is assumed that the Codecov repository
   upload token in the Travis build is stored in the :bash:`${CODECOV_TOKEN}`
   environment variable (securely defined in the Travis repository settings
   page). Travis build artifacts can be transferred to Dropbox using the
   `Dropbox Uploader <https://github.com/andreafabrizi/Dropbox-Uploader>`_
   script (included for convenience in the :bash:`${PCSV_DIR}/sbin` directory).
   For an automatic transfer that does not require manual entering of
   authentication credentials place the APPKEY, APPSECRET, ACCESS_LEVEL,
   OAUTH_ACCESS_TOKEN and OAUTH_ACCESS_TOKEN_SECRET values required by
   Dropbox Uploader in the in the :bash:`${DBU_APPKEY}`,
   :bash:`${DBU_APPSECRET}`, :bash:`${DBU_ACCESS_LEVEL}`,
   :bash:`${DBU_OAUTH_ACCESS_TOKEN}` and
   :bash:`${DBU_OAUTH_ACCESS_TOKEN_SECRET}` environment variables,
   respectively (also securely defined in Travis repository settings page)


9. Document the new feature or bug fix (if needed). The script
   :bash:`${PCSV_DIR}/sbin/build_docs.py` re-builds the whole package
   documentation (re-generates images, cogs source files, etc.):

        .. [[[cog ste('build_docs.py -h', 0, mdir, cog.out) ]]]

        .. code-block:: bash

            $ ${PUTIL_DIR}/sbin/build_docs.py -h
            usage: build_docs.py [-h] [-d DIRECTORY] [-r]
                                 [-n NUM_CPUS] [-t]

            Build pcsv package documentation

            optional arguments:
              -h, --help            show this help message and exit
              -d DIRECTORY, --directory DIRECTORY
                                    specify source file directory
                                    (default ../pcsv)
              -r, --rebuild         rebuild exceptions documentation.
                                    If no module name is given all
                                    modules with auto-generated
                                    exceptions documentation are
                                    rebuilt
              -n NUM_CPUS, --num-cpus NUM_CPUS
                                    number of CPUs to use (default: 1)
              -t, --test            diff original and rebuilt file(s)
                                    (exit code 0 indicates file(s) are
                                    identical, exit code 1 indicates
                                    file(s) are different)


        .. [[[end]]]

    Output of shell commands can be automatically included in reStructuredText
    source files with the help of Cog_ and the :code:`docs.support.term_echo` module.

    .. autofunction:: docs.support.term_echo.ste
        :noindex:

    .. autofunction:: docs.support.term_echo.term_echo
        :noindex:

    Similarly Python files can be included in docstrings with the help of Cog_
    and the :code:`docs.support.incfile` module

    .. autofunction:: docs.support.incfile.incfile
        :noindex:

.. rubric:: Footnotes

.. [#f1] All examples are for the `bash <https://www.gnu.org/software/bash/>`_
   shell

.. [#f2] It appears that Scipy dependencies do not include Numpy (as they
   should) so running the tests via Setuptools will typically result in an
   error. The pcsv requirement file specifies Numpy before Scipy and this
   installation order is honored by Tox so running the tests via Tox sidesteps
   Scipy's broken dependency problem but requires Tox to be installed before
   running the tests (Setuptools installs Tox if needed)

.. [#f3] It is assumed that all the Python interpreters are in the executables
   path. Source code for the interpreters can be downloaded from Python's main
   `site <http://www.python.org/downloads>`_

.. [#f4] Tox configuration largely inspired by
   `Ionel's codelog <http://blog.ionelmc.ro/2015/04/14/
   tox-tricks-and-patterns/>`_

.. include:: ../CHANGELOG.rst

License
=======

.. include:: ../LICENSE

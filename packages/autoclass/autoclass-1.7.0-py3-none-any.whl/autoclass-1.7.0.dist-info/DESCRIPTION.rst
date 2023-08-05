python-autoclass
================

|Build Status| |Tests Status| |codecov| |Documentation| |PyPI|

Project page : https://smarie.github.io/python-autoclass/

What's new in the development process
-------------------------------------

-  Improved documentation structure, and no longer hosted on readthedocs
-  Travis and codecov integration
-  Doc now generated from markdown using
   `mkdocs <http://www.mkdocs.org/>`__

Want to contribute ?
--------------------

Contributions are welcome ! Simply fork this project on github, commit
your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics:
https://github.com/smarie/python-autoclass/issues

Running the tests
-----------------

This project uses ``pytest``.

.. code:: bash

    pytest -v autoclass/tests/

You may need to install requirements for setup beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-test.txt

Packaging
---------

This project uses ``setuptools_scm`` to synchronise the version number.
Therefore the following command should be used for development snapshots
as well as official releases:

.. code:: bash

    python setup.py egg_info bdist_wheel rotate -m.whl -k3

You may need to install requirements for setup beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-setup.txt

Generating the documentation page
---------------------------------

This project uses ``mkdocs`` to generate its documentation page.
Therefore building a local copy of the doc page may be done using:

.. code:: bash

    mkdocs build

You may need to install requirements for doc beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-doc.txt

Generating the test reports
---------------------------

The following commands generate the html test report and the associated
badge.

.. code:: bash

    pytest --junitxml=junit.xml -v autoclass/tests/
    ant -f ci_tools/generate-junit-html.xml
    python ci_tools/generate-junit-badge.py

PyPI Releasing memo
~~~~~~~~~~~~~~~~~~~

This project is now automatically deployed to PyPI when a tag is
created. Anyway, for manual deployment we can use:

.. code:: bash

    twine upload dist/* -r pypitest
    twine upload dist/*

.. |Build Status| image:: https://travis-ci.org/smarie/python-autoclass.svg?branch=master
   :target: https://travis-ci.org/smarie/python-autoclass
.. |Tests Status| image:: https://smarie.github.io/python-autoclass/junit/junit-badge.svg?dummy=8484744
   :target: https://smarie.github.io/python-autoclass/junit/report.html
.. |codecov| image:: https://codecov.io/gh/smarie/python-autoclass/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/smarie/python-autoclass
.. |Documentation| image:: https://img.shields.io/badge/docs-latest-blue.svg
   :target: https://smarie.github.io/python-autoclass/
.. |PyPI| image:: https://img.shields.io/badge/PyPI-autoclass-blue.svg
   :target: https://pypi.python.org/pypi/autoclass/



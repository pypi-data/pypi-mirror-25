=============
Easy graphviz
=============


.. image:: https://img.shields.io/pypi/v/easygv.svg
        :target: https://pypi.python.org/pypi/easygv

.. image:: https://img.shields.io/travis/xguse/easygv.svg
        :target: https://travis-ci.org/xguse/easygv

.. image:: https://readthedocs.org/projects/easygv/badge/?version=latest
        :target: https://easygv.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/xguse/easygv/shield.svg
     :target: https://pyup.io/repos/github/xguse/easygv/
     :alt: Updates


Define nodes and edges in an excel file and graph-style attributes in a yaml file with inheritence.


* Free software: MIT license
* Documentation: https://easygv.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage




v0.1.0 / 2017-09-07
===================

  * tests more robust
  * Makefile: docs -> dont run apidoc as command
  * add_edges now supports edge labels and classes
  * easygv: added and improved docstrings
  * supports clusters
  * load_graph_input: now recodes NaNs to ""
  * configure flake8 ignores ignore flake8 D301 in certain functions flake8 ignore all E501, D413
  * easygv.cli: removed unused imports
  * inform that we only support py34 to py36
  * Fleshed out usage.rst

v0.0.2 / 2017-08-28
===================

  * docs/index.rst fixed title warning
  * delete cli.draw
  * add sphinx_rtd_theme as dev dep
  * tox.ini removed py2k added py36
  * first minimally functional commit
  * docs/conf.py set run_apidoc module_path
  * ran travis_pypi_setup.py
  * ignore tmp/

v0.0.1 (2017-08-25)
===================

* Initial commits.



package-name
------------
A very simple scaffold for constructing python packages


Installation
============
* run ``pip install python-git-package``


Introduction
============
This package can be used for scaffolding new packages.
The command ``pgp init`` creates a new package in the current folder.
The command ``pgp release`` creates a new release.
The command ``pgp doc`` builds the docs using sphinx.

The package layout is as follows:

.. code:: bash
    
    mypackage
     |-- .git
     |-- doc
     |    |--source
     |        |-- _static
     |        |-- _templates
     |        |-- conf.py
     |        |-- index.rst
     |        |-- mypackage.rst
     |
     |-- examples
     |-- mypackage
     |    |-- __init__.py
     |    |-- __version__.py
     |    |-- mypackage.py
     |
     |-- tests
     |    |-- all.py
     |    |-- test_mypackage.py
     |
     |-- .gitignore
     |-- LICENSE
     |-- MANIFEST.in
     |-- README.rst
     |-- setup.py

All files are populated with basic content so the notorious task of manually creating ``setup.py```or ``manifest.in`` is taken out of the users task.

Furthermore, the init command initializes a git repository with two branches, ``master`` and ``dev`` in the package folder.
The ``master`` branch is intended for published releases only.
It should allwats point to the latest release.
The ``dev`` branch is used for develloping the package.
To ease the process of creating a new release 



 
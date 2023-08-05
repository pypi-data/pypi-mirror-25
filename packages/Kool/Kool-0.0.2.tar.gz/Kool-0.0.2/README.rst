Kool
====

|CircleCI| |codecov| |Documentation Status|

Kool is an open source platform for online classroom management.

The aim is to create a minimalist framework that educationist can extend
when building an online classroom management system.

The current version supports extending class User, Course, and Quiz. The
database is a small CSV flatfile implementation.

Getting Started
---------------

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

Prerequisites
~~~~~~~~~~~~~

-  Python3. See `Python3
   Tutorial <https://docs.python.org/3/tutorial/>`__
-  Virtualenv. See `Virtual Environments
   Tutorial <https://docs.python.org/3/tutorial/venv.html>`__
-  Pip. See `Quickstart to installing Python
   modules <https://pip.pypa.io/en/stable/quickstart/>`__

Installing
~~~~~~~~~~

1. Fetch the latest copy of the project from github

::

    git clone https://github.com/edasi/kool.git

2. Setup a virtual environment

::

    python3 -m venv kool-env

On Windows, run:

::

    kool-env\Scripts\activate.bat

On Unix or MacOS, run:

::

    source kool-env/bin/activate

3. Install requirements

::

    pip install -U pip
    pip install -r requirements.txt

Code Examples
~~~~~~~~~~~~~

On python interactive shell, start by extending class User to create a
Student.

.. code:: python

    from kool.contrib.auth import User

    # Extending class User
    class Student(User):
        pass

    student = Student(first_name='John', last_name='Doe', email='john@doe.com', password='secretpwd')

    student.save()

To insert another student record in an existing table

.. code:: python

    from kool.db.models import table

    # Get Student table to perform CRUD operations
    student = table(Student)

    student.insert({'first_name': 'Mary', 'last_name': 'Doe', 'email': 'mary@doe.com', 'password': 'secretpwd2'})

To query an existing table

.. code:: python

    from kool.db.models import where

    student.filter(where('last_name') == 'Doe')

To perform complex queries

.. code:: python

    from kool.db.flatfile import Query

    Student = Query()

    student.filter((Student.first_name == 'John') | (Student.first_name == 'Mary'))

Tests
-----

Written tests are inside the tests/ directory. They are implemented
using the pytest module.

On a terminal, run:

::

    pytest tests/

Test Coverage
~~~~~~~~~~~~~

Test coverage is covered by
`coverage <https://coverage.readthedocs.io/en/coverage-4.4.1/index.html>`__
and `pytest-cov <https://github.com/pytest-dev/pytest-cov>`__ tools.
Local test reports are built in html format inside the htmlcov/
directory that is automatically generated when pytest is run. However,
online test reports are built by
`CircleCI <https://circleci.com/gh/edasi/kool/>`__

Related projects
----------------

-  `Blackboard <http://www.blackboard.com/>`__
-  `Canvas <https://www.canvaslms.com/>`__
-  `Chamilo <https://chamilo.org/es/>`__
-  `Moodle <https://moodle.org/>`__
-  `OpenEDX <https://github.com/edx/edx-platform>`__
-  `OpenSWAD <https://openswad.org/>`__
-  `Privacy preserving data
   publishing <https://github.com/rain1/Privacy-Preserving-Data-Publishing>`__
-  `Pygrades <https://bitbucket.org/jjauhien/pygrades>`__
-  `List on
   Wikipedia <https://en.wikipedia.org/wiki/List_of_learning_management_systems>`__

Documentation
-------------

Read the latest project documentation at
`kool-docs <http://kool-docs.readthedocs.io/en/latest/>`__

License
-------

Kool is licensed under `MIT
License <https://github.com/edasi/kool/blob/master/LICENSE>`__

.. |CircleCI| image:: https://circleci.com/gh/edasi/kool/tree/master.svg?style=shield
   :target: https://circleci.com/gh/edasi/kool/tree/master
.. |codecov| image:: https://codecov.io/gh/edasi/kool/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/edasi/kool
.. |Documentation Status| image:: https://readthedocs.org/projects/kool-docs/badge/?version=latest
   :target: http://kool-docs.readthedocs.io/en/latest/?badge=latest
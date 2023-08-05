raster-foundry-python-client
============================

A Python client for `Raster Foundry <https://www.rasterfoundry.com/>`_, a web platform for combining, analyzing, and publishing raster data.

Usage
-----

.. code-block:: python

   from rf.api import API
   refresh_token = '<>'

   api = API(refresh_token=refresh_token)

   # List all projects
   my_projects = api.projects

   one_project = my_projects[0]

   # Get TMS URl without token
   one_project.tms()


Installation
------------

.. code:: bash

   $ pip install rasterfoundry


Testing
-------

The test suite execution process is managed by ``tox``:

.. code:: bash

   $ tox


Releases
--------

Releases are automatically published to PyPI through Travis CI when commits are tagged. The following ``git flow`` commands lead to a tagged commit that can be pushed to GitHub:


.. code:: bash

   $ git flow release start X.Y.Z
   $ vim CHANGELOG.rst
   $ vim setup.py
   $ git commit -m "X.Y.Z"
   $ git flow release publish X.Y.Z
   $ git flow release finish X.Y.Z


After you've completed the ``git flow`` steps above, you'll need to push the changes from your local repository to the GitHub repository:

.. code:: bash

   $ git checkout develop
   $ git push origin develop
   $ git checkout master
   $ git push origin master
   $ git push --tags

=============================
Django Workflow FSM
=============================

.. image:: https://badge.fury.io/py/django-workflow-fsm.svg
    :target: https://badge.fury.io/py/django-workflow-fsm

.. image:: https://travis-ci.org/george-silva/django-workflow-fsm.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-workflow-fsm

.. image:: https://codecov.io/gh/george-silva/django-workflow-fsm/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-workflow-fsm

Control FSMs from Django

Documentation
-------------

The full documentation is at https://django-workflow-fsm.readthedocs.io.

Quickstart
----------

Install Django Workflow FSM::

    pip install django-workflow-fsm

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'workflow.apps.WorkflowConfig',
        ...
    )

Add Django Workflow FSM's URL patterns:

.. code-block:: python

    from workflow import urls as workflow_urls


    urlpatterns = [
        ...
        url(r'^', include(workflow_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

You need to have postgresql installed, with user/password postgres/postgres.

You will also need REDIS installed and working. This package for testing
will use the default redis configuration, localhost, 6379 port and 0 database.

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

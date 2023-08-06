=========================
Websauna Jinja2 Extension
=========================

.. |ci| image:: https://travis-ci.org/websauna/websauna.j2secret.svg
    :target: https://travis-ci.org/websauna/websauna.j2secret/

.. |latest| image:: https://img.shields.io/pypi/v/websauna.j2secret.svg
    :target: https://pypi.python.org/pypi/websauna.j2secret/
    :alt: Latest Version

.. |license| image:: https://img.shields.io/pypi/l/websauna.j2secret.svg
    :target: https://pypi.python.org/pypi/websauna.j2secret/
    :alt: License

.. |cov| image:: https://codecov.io/github/websauna/websauna.j2secret/coverage.svg?branch=master
    :target: https://codecov.io/github/websauna/websauna.j2secret?branch=master


.. |versions| image:: https://img.shields.io/pypi/pyversions/websauna.j2secret.svg
    :target: https://pypi.python.org/pypi/websauna.j2secret/
    :alt: Supported Python versions


This is a Jinja2 extension required by Cookiecutter Websauna templates.

+-----------+-----------+-----------+
| |ci|      ||cov|      |           |
+-----------+-----------+-----------+
| |versions|| |latest|  ||license|  |
+-----------+-----------+-----------+

.. contents:: :local:


Installation
============

Using the same virtualenv where cookiecutter is installed install this extension executing pip install:

.. code-block:: shell

    pip install websauna.j2secret


Usage
=====

Extend the Cookiecutter environment with this custom `Jinja2 extensions`_,
that adds a tag named **secret** , specifing the **websauna.j2secret** extension in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "authentication_random": "{% secret() %}",
        "authomatic_random": "{% secret() %}",
        "session_random": "{% secret() %}",
        "_extensions": ["websauna.j2secret.SecretExtension"]
    }


Read more about `Template Extensions for Cookiecutter`_.


Running the test suite
======================

Install test and dev dependencies (run in the folder with ``setup.py``)::

    pip install -e ".[test]"

Run test suite using py.test running::

    py.test

More information
================

Please see https://websauna.org/


.. _`Jinja2 extensions`: http://jinja2.readthedocs.io/en/latest/extensions.html#extensions
.. _`Template Extensions for Cookiecutter`: http://cookiecutter.readthedocs.io/en/latest/advanced/template_extensions.html

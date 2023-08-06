Zenaton client library
======================

This is the official Python client library for Zenaton (https://zenaton.com/).

.. image:: https://travis-ci.org/zenaton/zenaton-python.svg?branch=master
    :target: https://travis-ci.org/zenaton/zenaton-python


Requirements
------------

Supported Python versions are 2.7 and 3.3+.


Installing
----------

Install the latest stable release using ``pip``:

.. code-block:: shell

    $ pip install zenaton

Alternatively, you can install the latest development version from GitHub:

.. code-block:: shell

    $ pip install -e git+https://github.com/zenaton/zenaton-python.git#egg=zenaton


Getting started
---------------

#) In a first terminal, download and start the Zenaton worker:

   .. code-block:: shell

    $ cd /path/to/my/project
    $ curl -O https://zenaton.com/dist/zenaton_worker
    $ chmod +x zenaton_worker
    $ ./zenaton_worker

#) In another terminal, create a `virtualenv`_ for your project
   and activate it:

   .. code-block:: shell

      $ cd /path/to/my/project
      $ virtualenv venv
      $ source venv/bin/activate

#) Get the Zenaton Python examples:

   .. code-block:: shell

      $ git clone https://github.com/zenaton/examples-python.git
      $ cd examples-python
      $ pip install -e .

#) Go to your Zenaton `dashboard`_ to get your application ID and an API token:

   .. code-block:: shell

      $ export ZENATON_APP_ID=<your application id>
      $ export ZENATON_API_TOKEN=<your api token>
      $ export ZENATON_APP_ENV=dev

#) Send the config to the Zenaton worker:

   .. code-block:: shell

      $ zenaton_init

#) Launch an example:

   .. code-block:: shell

      $ python zenaton_examples/launch_sequential.py

.. _dashboard: https://zenaton.com/app/api
.. _virtualenv: https://virtualenv.pypa.io/

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


Getting started
---------------

.. code-block:: python

    #
    # Getting started with Zenaton
    #
    from zenaton import Client, Task, Workflow


    class Echo(Task):

        def __init__(self, value):
            self.value = value

        def handle(self):
            print(self.value)


    class MyWorkflow(Workflow):

        def __init__(self, count):
            self.count = count

        def handle(self):
            while self.count > 0:
                self.execute(Echo(self.count))
                self.count -= 1


    if __name__ == '__main__':

        # Create a simple workflow
        workflow = MyWorkflow(count=10)

        # Ask Zenaton to start an instance of this workflow
        client = Client(app_id='APP_ID', token='API_TOKEN', environment='APP_ENV')
        instance = client.start(workflow)
        print(instance.id)


Hacking
-------

Run tests using ``py.test``:

.. code-block:: shell

    $ pip install -r requirements-testing.txt
    $ py.test

Run tests on all supported Python versions using ``tox``:

.. code-block:: shell

    $ pip install tox
    $ tox


Documentation
-------------

Build the docs using Sphinx:

.. code-block:: shell

    $ pip install sphinx sphinxcontrib-napoleon
    $ cd docs
    $ make html

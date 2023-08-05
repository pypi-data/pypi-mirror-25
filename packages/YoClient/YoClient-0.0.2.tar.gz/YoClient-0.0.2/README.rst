Yo RPC API Client
=================

|Build Status| |codecov|

Introduction
------------

This is a Python client for the `Yo RPC
API <http://docs.justyo.co/docs/yo>`__.

Installation
------------

``pip install yo_client``

Usage
-----

Instantiation
~~~~~~~~~~~~~

Instantiate a client by passing an API Key in the constructor

.. code:: python

    client = YoClient("some_api_key")

Send a Yo
~~~~~~~~~

Send a Yo to a user with optional text and an optional link or
coordinate. Currently, the Yo API allows either a link or coordinate to
be sent with a Yo, but not both.

.. code:: python

    client = YoClient("some_api_key")
    response = client.send_yo(username="some_username", text="some_text", link="some_link")

Send a Yo to All Subscribers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Send a Yo to all subscribers - the only value to pass this method is a
link.

.. code:: python

    client = YoClient("some_api_key")
    response = client.send_yo_to_all_subscribers(link="some_link")

Create a Yo Account
~~~~~~~~~~~~~~~~~~~

.. code:: python

    client = YoClient("some_api_key")
    response = client.create_account(username="some_username")

Check if a Username Exists
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client = YoClient("some_api_key")
    response = client.username_exists(username="some_username")

Get Subscribers Count
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client = YoClient("some_api_key")
    response = client.get_subscribers_count()

.. |Build Status| image:: https://travis-ci.org/jaebradley/yo_client.svg?branch=master
   :target: https://travis-ci.org/jaebradley/yo_client
.. |codecov| image:: https://codecov.io/gh/jaebradley/yo_client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jaebradley/yo_client

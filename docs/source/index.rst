falcon-graphene
===============

Welcom to falcon-graphene! This library provides a small set of helpers for
serving a GraphQL API surface with Falcon_. It can be used alongside an
existing Falcon API, or as the sole HTTP API surface. By leveraging Falcon's
existing framework features, you get to:

* Bring all of your existing middleware, hooks, routing, etc.
* Leverage Falcon's `request context`_ in your Graphene ``resolve_*`` methods.
* Have a |really fast|_ GraphQL API.

.. _Falcon: https://falconframework.org
.. _request context: https://falcon.readthedocs.io/en/stable/api/request_and_response.html#Request.context
.. _really fast: https://falconframework.org/index.html#Metrics

.. |really fast| replace:: *really fast*

.. toctree::
   :maxdepth: 2
   :caption: Contents:


API Reference
=============

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

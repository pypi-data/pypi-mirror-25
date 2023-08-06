Relevance: Content pipeline manager
###################################

Relevance is a content pipeline management suite. Its goal is to provide tools and
interfaces for ingesting content, obtaining relevant search results and
providing useful analytics on its usage.

This software is still under heavy development, and is available for preview.
Contributions are welcome.

.. contents::

.. section-numbering::

Features
========

Current features
----------------

- Federated search across ElasticSearch indices
- Simple configuration
- Simple query language
- Simple query API
- Mapping API
- Command line tools

Upcoming features
-----------------

- Ingestion API
- Crawler integration

Planned features
----------------

- NLP integration
- Security layer
- Configuration API
- Query extensions
- MySQL support
- Postgres support
- Analytics
- Machine learning
- SQLite support

Installation
============

The fastest way to install is to retrieve the release tarball using ``git``, and
install using ``pip``:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools
    $ pip install relevance

Requirements
------------

Currently, a running instance of ElasticSearch 2.x is required.

Python version
--------------

Although Python 3+ should work, all development is done on Python 3.6.2.
As such, only 3.6 and newer is currently officially supported.

Usage
=====

First, createa your configuration files:

.. code-block:: bash

    $ cp /etc/search.json-example /etc/search.json

Then start the server:

.. code-block:: bash

    $ relevance-server -v

Then query away:

.. code-block:: bash

    $ curl -XGET 'http://localhost:5346/myEngine?q="toast"'

The query language is simple and reminiscent of Python expressions:

.. code-block::

    ("term1" or "term2") and str_facet=="value" and interval_facet>10 and other==None

The simple query language support additional options:

.. code-block::

    "search expr" with slice(10, 10) with sort(date, desc) with facet(popularity, author)

You can also limit search to specific document types:

.. code-block::

    "search" or "term" with type(tweet, article)

The options, query terms and facets can be mixed and matched.

You can get a list of instances using:

.. code-block:: bash

    $ curl -XGET 'http://localhost:5346/'

You can fetch the document types for a specific instance:

.. code-block:: bash

    $ curl -XGET 'http://localhost:5346/myEngine/mapping'

...and you can describe the mapping for that document type:

.. code-block:: bash

    $ curl -XGET 'http://localhost:5346/myEngine/mapping/tweet'

Contributing
============

Contributions are always welcome. If you want to contribute:

- Fork the project
- Test your code (see below)
- Push your code
- Submit a pull request

Testing
-------

Contributions must pass both the tests and styling guidelines. Before submitting a patch,
make sure you run:

.. code-block:: bash

    $ ./setup.py flake8
    $ ./setup.py test

About the project
=================

Change log
----------

MIT License: see `LICENSE <https://bitbucket.org/overridelogic/relevance/raw/master/CHANGELOG.rst>`_.


Licence
-------

MIT License: see `LICENSE <https://bitbucket.org/overridelogic/relevance/raw/master/LICENSE>`_.


Authors
-------

**Francis Lacroix** `@netcoder1` created Relevance while at **OverrideLogic**.

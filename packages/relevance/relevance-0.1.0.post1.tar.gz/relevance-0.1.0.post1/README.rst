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

Upcoming features
-----------------

- Mapping API
- SQLite support

Planned features
----------------

- Ingestion API
- Crawler integration
- Query extensions
- MySQL support
- Postgres support
- Analytics
- Machine learning

Installation
============

The fastest way to install is to retrieve the release tarball using ``git``, and
install using ``pip``:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools

    # Create the directory and extract the application:
    $ mkdir relevance/ && cd relevance/
    $ git archive --remote ssh://git@bitbucket.org/overridelogic/relevance.git master \
        --format tar.gz | tar -zxvf -

    # Install the dependencies and the application.
    # You may want to pass the --user switch or run this as root (not recommended).
    $ pip install --user -r requirements.txt


Python version
--------------

Although Python 3+ should work, all development is done on Python 3.6.2.
As such, only 3.6 and newer is currently officially supported.

Unstable version
----------------

You can also instead of the latest the latest unreleased development version
directly from the ``develop`` branch on BitBucket.

It is a work-in-progress of a future stable release so the experience
might be not as smooth.

Usage
=====

First, create a configuration file:

.. code-block:: bash

    $ cat > etc/default.json <<EOF                                    
    {                        
      "myEngine": {
        "engine": "relevance.engine.elastic.ElasticSearchEngine",
        "target": "http://localhost:9200",       
        "facets": {                  
          "author": {
            "type": "relevance.facet.TermFacet",
            "field": "author"    
          },
          "categories": {
            "type": "relevance.facet.TermFacet",    
            "path": "categories.name"
          },
          "created_date": {
            "type": "relevance.facet.DateFacet", 
            "field": "createdAt",
            "options": {"interval": "month"}
          },             
          "votes": {               
            "type": "relevance.facet.IntervalFacet",
            "field": "voteCount",      
            "options": {"interval": 100}
          },   
          "popularity": {
            "type": "relevance.facet.RangeFacet",
            "field": "viewCount",
            "options": {
              "ranges": {
                "Meh": [null, 100],
                "Okay": [100, 1000],
                "Great": [1000, 10000],
                "Wow": [10000, null]
              }
            }
          }
        }
      }
    }
    EOF

Then start the server:

.. code-block:: bash

    $ python3 -m relevance.api.search

Then query away:

.. code-block:: bash

    $ curl -XGET 'http://localhost:5000/myEngine?q="toast"'

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

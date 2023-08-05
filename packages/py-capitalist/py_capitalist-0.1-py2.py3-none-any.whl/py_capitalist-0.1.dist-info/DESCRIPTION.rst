PyCapitalist
============

.. image:: https://travis-ci.org/Stranger6667/py-capitalist.svg?branch=master
   :target: https://travis-ci.org/Stranger6667/py-capitalist
   :alt: Build Status

.. image:: https://codecov.io/github/Stranger6667/py-capitalist/coverage.svg?branch=master
   :target: https://codecov.io/github/Stranger6667/py-capitalist?branch=master
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/py-capitalist/badge/?version=stable
   :target: http://py-capitalist.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/py-capitalist.svg
    :target: https://pypi.python.org/pypi/py-capitalist
    :alt: Latest PyPI version

Python client library for `Capitalist API <https://capitalist.net/developers/api>`_.

Installation
============

PyCapitalist can be obtained with ``pip``::

    $ pip install py-capitalist

Usage example
=============

.. code-block:: python

    >>> from capitalist import CapitalistClient
    >>> capitalist = CapitalistClient(username='user', password='pass')
    >>> capitalist.currency_rates()
    {'code': 0,
     'data': {'rates': {'buy': [{'amount': 1.15,
         'amountCur': 'USD',
         'target': 'EUR'},
        {'amount': 3874.15, 'amountCur': 'USD', 'target': 'BTC'},
        {'amount': 3262.95, 'amountCur': 'EUR', 'target': 'BTC'},
        {'amount': 228094.87, 'amountCur': 'RUR', 'target': 'BTC'},
        {'amount': 57.32, 'amountCur': 'RUR', 'target': 'USD'},
        {'amount': 67.52, 'amountCur': 'RUR', 'target': 'EUR'}],
       'sell': [{'amount': 1.26, 'amountCur': 'USD', 'target': 'EUR'},
        {'amount': 4070.33, 'amountCur': 'USD', 'target': 'BTC'},
        {'amount': 3428.17, 'amountCur': 'EUR', 'target': 'BTC'},
        {'amount': 239808.15, 'amountCur': 'RUR', 'target': 'BTC'},
        {'amount': 59.11, 'amountCur': 'RUR', 'target': 'USD'},
        {'amount': 70.94, 'amountCur': 'RUR', 'target': 'EUR'}]}},
     'message': ''}

Documentation
=============

You can view the documentation online at:

- https://py-capitalist.readthedocs.io/en/stable/

Or you can look at the docs/ directory in the repository.

Python support
==============

PyCapitalist supports Python 2.7, 3.3, 3.4, 3.5, 3.6.



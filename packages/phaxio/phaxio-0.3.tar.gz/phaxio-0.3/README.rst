Phaxio
======

|PyPI| |GitHub license|

A Python module for interacting with the `Phaxio API`_.

Installation
------------

Via pip:

::

    $ pip install phaxio


Full Documentation
------------------

http://phaxio-python.readthedocs.io/en/latest/

Usage
-----

Send a fax to multiple people using HTML message:

.. code:: python

    from phaxio import PhaxioApi

    api = PhaxioApi(key, secret)
    response = api.Fax.send(to=['4141234567', '5141234567', '6151234567'],
        files='/path/to/supported/file.pdf')
    print(response.data.id)

The full set of Phaxio APIs is available and split into functional groups:

::

    api.Fax

    api.PhoneNumber

    api.PhaxCode

    api.Account

    api.Countries

Generally, each supported method takes keyword arguments with the exact
same names of the API method parameters as they’re described in the
`Phaxio documentation`_.

See the `tests`_ for additional examples, or the `full documentation`_.

Error Handling
~~~~~~~~~~~~~~

Errors will cause an ``ApiException``, with fields for HTTP status code, reponse headers, and json response data in the body.


Testing
-------

::

    export API_KEY="MY_API_KEY"
    export API_SECRET="MY_API_SECRET"
    python setup.py test


Contributing
============

Making API changes
------------------

#. Make changes to ``spec/api.yaml``
#. Run ``make swagger-generate``
#. Make changes to ``phaxio/api.py`` as necessary
#. Update documentation if necessary

- ``docs/source/phaxio.rst`` will probably not require updates unless it's a very big change
- ``docs/source/models.rst`` will require updates only if there are new model types


.. _Phaxio API: https://www.phaxio.com/docs
.. _full documentation: http://phaxio-python.readthedocs.io/en/latest/
.. _Phaxio documentation: https://www.phaxio.com/docs
.. _tests: tests/test_api.py
.. |PyPI| image:: https://img.shields.io/pypi/v/phaxio.svg
    :target: https://pypi.python.org/pypi/phaxio
.. |GitHub license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://github.com/anpolsky/phaxio-python/blob/master/LICENSE
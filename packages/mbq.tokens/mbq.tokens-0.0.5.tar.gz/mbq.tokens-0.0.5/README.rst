mbq.tokens: fool-proof token decoding
=====================================

.. image:: https://img.shields.io/pypi/v/mbq.tokens.svg
    :target: https://pypi.python.org/pypi/mbq.tokens

.. image:: https://img.shields.io/pypi/l/mbq.tokens.svg
    :target: https://pypi.python.org/pypi/mbq.tokens

.. image:: https://img.shields.io/pypi/pyversions/mbq.tokens.svg
    :target: https://pypi.python.org/pypi/mbq.tokens

.. image:: https://img.shields.io/travis/managedbyq/mbq.tokens/master.svg
    :target: https://travis-ci.org/managedbyq/mbq.tokens

Installation
------------

.. code-block:: bash

    $ pip install mbq.tokens
    🚀✨

Guaranteed fresh.


Getting started
---------------

.. code-block:: python

    from mbq import tokens

    tokens.init(
        certificate=settings.FORMATTED_CERTIFICATE,
        allowed_audiences=set(settings.ALLOWED_AUDIENCES),
    )

    try:
        decoded_token = tokens.decode(token)
    except tokens.TokenError:
        # will only ever raise TokenError
        logger.exception('Failed to decode token')

    decoded_token = tokens.decode_header(request.META['HTTP_AUTHORIZATION'])

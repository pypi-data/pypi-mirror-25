Schematizer
===========

Schematizer is a lightweight library for data marshalling/unmarshalling in Python.

It helps you:

- **Validate** input and output data
- **Marshal** primitive data into a form you would like to interact with
- **Unmarshal** native data so that it can be rendered to JSON, YAML, MsgPack, etc.

Examples
--------

Simple.

.. code:: python

    >>> from schematizer.exceptions import BaseValidationError
    >>> from schematizer.nodes.compound import Dict, List
    >>> from schematizer.nodes.simple import Date, Str
    >>> from schematizer.validators import Length
    >>>
    >>> album_schema = Dict({
    ...    'title': Str(),
    ...    'released_at': Date(),
    ... })
    >>>
    >>> artist_schema = Dict({
    ...     'name': Str(),
    ...     'albums': List(album_schema),
    ... })
    >>>
    >>> artist_schema.to_native({
    ...     'name': 'Burzum',
    ...     'albums': [
    ...         {
    ...             'title': 'Filosofem',
    ...             'released_at': '1996-01-01',
    ...         },
    ...     ],
    ... })
    {'name': 'Burzum', 'albums': [{'title': 'Filosofem', 'released_at': datetime.date(1996, 1, 1)}]}

With invalid data.

.. code:: python

    >>> try:
    ...     artist_schema.to_native({
    ...         'albums': [
    ...             {'released_at': '19960101'},
    ...         ],
    ...     })
    ... except BaseValidationError as exc:
    ...     exc.flatten()
    ...
    [
        SimpleValidationError('MISSING', path=['name'], extra=None),
        SimpleValidationError('MISSING', path=['albums', 0, 'title'], extra=None),
        SimpleValidationError('INVALID', path=['albums', 0, 'released_at'], extra={'message': "time data '19960101' does not match format '%Y-%m-%d'"}),
    ]

Installation
------------

::

    $ pip install schematizer

Documentation
-------------

Coming soon...

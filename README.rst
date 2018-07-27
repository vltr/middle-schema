=================
``middle-schema``
=================

.. start-badges

A lot of badges from the ``cookiecutter`` template I used. I think I'll get rid of a lot of them in the near future.

.. image:: https://readthedocs.org/projects/middle-schema/badge/?style=flat
    :target: https://readthedocs.org/projects/middle-schema
    :alt: Documentation Status

.. image:: https://travis-ci.org/vltr/middle-schema.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/middle-schema

.. image:: https://ci.appveyor.com/api/projects/status/github/vltr/middle-schema?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vltr/middle-schema

.. image:: https://codecov.io/github/vltr/middle-schema/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/middle-schema

.. image:: https://api.codacy.com/project/badge/Grade/10c6ef32dfbe497087d57c9d86c02c80
    :alt: Codacy Grade
    :target: https://www.codacy.com/app/vltr/middle-schema?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vltr/middle-schema&amp;utm_campaign=Badge_Grade

.. image:: https://img.shields.io/pypi/v/middle-schema.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/pypi/pyversions/middle-schema.svg
    :alt: Supported versions
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/pypi/implementation/middle-schema.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/pypi/status/middle-schema.svg
    :alt: PyPI - Status
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. end-badges

Translate your middle model declarations to OpenAPI, JSONSchema or any other schema you need!

Quick peak
----------

.. code-block:: pycon

    >>> from typing import Dict, List
    >>> import middle

    >>> class Game(middle.Model):
    ...     name: str = middle.field()
    ...     score: float = middle.field(minimum=0, maximum=10)
    ...     resolution_tested: str = middle.field(pattern="^\d+x\d+$")
    ...     genre: List[str] = middle.field(unique_items=True)
    ...     rating: Dict[str, float] = middle.field(max_properties=5)

    >>> data = {
    ...     "name": "Cities: Skylines",
    ...     "score": 9.0,
    ...     "resolution_tested": "1920x1200",
    ...     "genre": ["Simulators", "City Building"],
    ...     "rating": {
    ...         "IGN": 8.5,
    ...         "Gamespot": 8.0,
    ...         "Steam": 4.5
    ...     }
    ... }

    >>> game = Game(**data)

    >>> game
    Game(name='Cities: Skylines', score=9.0, resolution_tested='1920x1200', genre=['Simulators', 'City Building'], rating={'IGN': 8.5, 'Gamespot': 8.0, 'Steam': 4.5})

    >>> middle.asdict(game)
    {'name': 'Cities: Skylines', 'score': 9.0, 'resolution_tested': '1920x1200', 'genre': ['Simulators', 'City Building'], 'rating': {'IGN': 8.5, 'Gamespot': 8.0, 'Steam': 4.5}}

.. warning::

    **IMPORTANT**: ``middle`` and ``middle-schema`` are in **very early stages** of development! Use with caution and be aware that some functionalities and APIs may change between versions until they're out of **alpha**.

Documentation
=============

https://middle-schema.readthedocs.io/en/latest/

License
=======

``middle-schema`` is a free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

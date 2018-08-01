=================
``middle-schema``
=================

.. start-badges

.. image:: https://img.shields.io/pypi/status/middle-schema.svg
    :alt: PyPI - Status
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/pypi/v/middle-schema.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/middle-schema/

.. image:: https://img.shields.io/pypi/pyversions/middle-schema.svg
    :alt: Supported versions
    :target: https://pypi.org/project/middle-schema/

.. image:: https://travis-ci.org/vltr/middle-schema.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/middle-schema

.. image:: https://ci.appveyor.com/api/projects/status/github/vltr/middle-schema?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vltr/middle-schema

.. image:: https://readthedocs.org/projects/middle-schema/badge/?style=flat
    :target: https://readthedocs.org/projects/middle-schema
    :alt: Documentation Status

.. image:: https://codecov.io/github/vltr/middle-schema/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/middle-schema

.. image:: https://api.codacy.com/project/badge/Grade/6425ac0a119f481bb4f2b269bd7f52fc
    :alt: Codacy Grade
    :target: https://www.codacy.com/app/vltr/middle-schema?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vltr/middle-schema&amp;utm_campaign=Badge_Grade

.. image:: https://pyup.io/repos/github/vltr/middle-schema/shield.svg
    :target: https://pyup.io/account/repos/github/vltr/middle-schema/
    :alt: Packages status

.. end-badges

Translate your `middle <https://middle.readthedocs.io/en/latest/>`_ model declarations to OpenAPI, JSONSchema or any other schema you need!

In a nutshell
-------------

.. code-block:: pycon

    >>> import enum
    >>> import json
    >>> import typing as t
    >>> import middle
    >>> from middle_schema.openapi import parse

    >>> @enum.unique
    ... class PlatformEnum(str, enum.Enum):
    ...     XBOX1 = "XBOX1"
    ...     PLAYSTATION4 = "PLAYSTATION4"
    ...     PC = "PC"

    >>> @enum.unique
    ... class LanguageEnum(enum.IntEnum):
    ...     ENGLISH = 1
    ...     JAPANESE = 2
    ...     SPANISH = 3
    ...     GERMAN = 4
    ...     PORTUGUESE = 5

    >>> @enum.unique
    ... class CityRegionEnum(str, enum.Enum):
    ...     TROPICAL = "TROPICAL"
    ...     TEMPERATE = "TEMPERATE"
    ...     BOREAL = "BOREAL"

    >>> class City(middle.Model):
    ...     __description__ = "One awesome city built"
    ...     name = middle.field(type=str, description="The city name")
    ...     region = middle.field(
    ...         default=CityRegionEnum.TEMPERATE,
    ...         type=CityRegionEnum,
    ...         description="The region this city is located",
    ...     )

    >>> class Player(middle.Model):
    ...     nickname = middle.field(
    ...         type=str, description="The nickname of the player over the internet"
    ...     )
    ...     youtube_channel = middle.field(
    ...         type=str, description="The YouTube channel of the player", default=None
    ...     )

    >>> class Game(middle.Model):
    ...     __description__ = "An electronic game model"
    ...     name = middle.field(type=str, description="The name of the game")
    ...     platform = middle.field(
    ...         type=PlatformEnum, description="Which platform it runs on"
    ...     )
    ...     score = middle.field(
    ...         type=float,
    ...         description="The average score of the game",
    ...         minimum=0,
    ...         maximum=10,
    ...         multiple_of=0.1,
    ...     )
    ...     resolution_tested = middle.field(
    ...         type=str,
    ...         description="The resolution which the game was tested",
    ...         pattern="^\d+x\d+$",
    ...     )
    ...     genre = middle.field(
    ...         type=t.List[str],
    ...         description="One or more genres this game is part of",
    ...         min_items=1,
    ...         unique_items=True,
    ...     )
    ...     rating = middle.field(
    ...         type=t.Dict[str, float],
    ...         description="Ratings given on specialized websites",
    ...         min_properties=3,
    ...     )
    ...     players = middle.field(
    ...         type=t.Set[str],
    ...         description="Some of the notorious players of this game",
    ...     )
    ...     language = middle.field(
    ...         type=LanguageEnum, description="The main language of the game"
    ...     )
    ...     awesome_city = middle.field(type=City)
    ...     remarkable_resources = middle.field(
    ...         type=t.Union[Player, City],
    ...         description="Some remarkable resources of this game over the internet",
    ...     )

    >>> api = parse(Game)

    >>> json.dumps(api.specification, indent=4, sort_keys=True)
    {
        "description": "An electronic game model",
        "properties": {
            "awesome_city": {
                "description": "One awesome city built",
                "properties": {
                    "name": {
                        "description": "The city name",
                        "type": "string"
                    },
                    "region": {
                        "choices": [
                            "TROPICAL",
                            "TEMPERATE",
                            "BOREAL"
                        ],
                        "description": "The region this city is located",
                        "type": "string"
                    }
                },
                "required": [
                    "name"
                ],
                "type": "object"
            },
            "genre": {
                "description": "One or more genres this game is part of",
                "items": {
                    "type": "string"
                },
                "minItems": 1,
                "type": "array",
                "uniqueItems": true
            },
            "language": {
                "choices": [
                    1,
                    2,
                    3,
                    4,
                    5
                ],
                "description": "The main language of the game",
                "format": "int64",
                "type": "integer"
            },
            "name": {
                "description": "The name of the game",
                "type": "string"
            },
            "platform": {
                "choices": [
                    "XBOX1",
                    "PLAYSTATION4",
                    "PC"
                ],
                "description": "Which platform it runs on",
                "type": "string"
            },
            "players": {
                "description": "Some of the notorious players of this game",
                "items": {
                    "properties": {
                        "nickname": {
                            "description": "The nickname of the player over the internet",
                            "type": "string"
                        },
                        "youtube_channel": {
                            "description": "The YouTube channel of the player",
                            "type": "string"
                        }
                    },
                    "required": [
                        "nickname"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "rating": {
                "additionalProperties": {
                    "format": "double",
                    "type": "number"
                },
                "description": "Ratings given on specialized websites",
                "minProperties": 3,
                "type": "object"
            },
            "remarkable_resources": {
                "anyOf": [
                    {
                        "properties": {
                            "nickname": {
                                "description": "The nickname of the player over the internet",
                                "type": "string"
                            },
                            "youtube_channel": {
                                "description": "The YouTube channel of the player",
                                "type": "string"
                            }
                        },
                        "required": [
                            "nickname"
                        ],
                        "type": "object"
                    },
                    {
                        "description": "One awesome city built",
                        "properties": {
                            "name": {
                                "description": "The city name",
                                "type": "string"
                            },
                            "region": {
                                "choices": [
                                    "TROPICAL",
                                    "TEMPERATE",
                                    "BOREAL"
                                ],
                                "description": "The region this city is located",
                                "type": "string"
                            }
                        },
                        "required": [
                            "name"
                        ],
                        "type": "object"
                    }
                ],
                "description": "Some remarkable resources of this game over the internet"
            },
            "resolution_tested": {
                "description": "The resolution which the game was tested",
                "pattern": "^\\d+x\\d+$",
                "type": "string"
            },
            "score": {
                "description": "The average score of the game",
                "format": "double",
                "maximum": 10,
                "minimum": 0,
                "multipleOf": 0.1,
                "type": "number"
            }
        },
        "required": [
            "name",
            "platform",
            "score",
            "resolution_tested",
            "genre",
            "rating",
            "players",
            "language",
            "awesome_city",
            "remarkable_resources"
        ],
        "type": "object"
    }


.. warning::

    **IMPORTANT**: ``middle`` and ``middle-schema`` are in **very early stages** of development! Use with caution and be aware that some functionalities and APIs may change between versions until they're out of **alpha**.

Documentation
=============

https://middle-schema.readthedocs.io/en/latest/

License
=======

``middle-schema`` is a free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

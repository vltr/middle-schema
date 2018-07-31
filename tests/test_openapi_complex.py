import enum
import typing as t

import middle

from middle_schema.openapi import OpenAPI
from middle_schema.openapi import parse


@enum.unique
class PlatformEnum(str, enum.Enum):
    XBOX1 = "XBOX1"
    PLAYSTATION4 = "PLAYSTATION4"
    PC = "PC"


@enum.unique
class LanguageEnum(enum.IntEnum):
    ENGLISH = 1
    JAPANESE = 2
    SPANISH = 3
    GERMAN = 4
    PORTUGUESE = 5


@enum.unique
class CityRegionEnum(str, enum.Enum):
    TROPICAL = "TROPICAL"
    TEMPERATE = "TEMPERATE"
    BOREAL = "BOREAL"


class City(middle.Model):
    __description__ = "One awesome city built"
    name = middle.field(type=str, description="The city name")
    region = middle.field(
        default=CityRegionEnum.TEMPERATE,
        type=CityRegionEnum,
        description="The region this city is located",
    )


class Player(middle.Model):
    nickname = middle.field(
        type=str, description="The nickname of the player over the internet"
    )
    youtube_channel = middle.field(
        type=str, description="The YouTube channel of the player", default=None
    )


class Game(middle.Model):
    __description__ = "An electronic game model"

    name = middle.field(type=str, description="The name of the game")
    platform = middle.field(
        type=PlatformEnum, description="Which platform it runs on"
    )
    score = middle.field(
        type=float,
        description="The average score of the game",
        minimum=0,
        maximum=10,
        multiple_of=0.1,
    )
    resolution_tested = middle.field(
        type=str,
        description="The resolution which the game was tested",
        pattern="^\d+x\d+$",
    )
    genre = middle.field(
        type=t.List[str],
        description="One or more genres this game is part of",
        min_items=1,
        unique_items=True,
    )
    rating = middle.field(
        type=t.Dict[str, float],
        description="Ratings given on specialized websites",
        min_properties=3,
    )
    players = middle.field(
        type=t.Set[Player],
        description="Some of the notorious players of this game",
    )
    language = middle.field(
        type=LanguageEnum, description="The main language of the game"
    )
    awesome_city = middle.field(type=City)
    remarkable_resources = middle.field(
        type=t.Union[Player, City],
        description="Some remarkable resources of this game over the internet",
    )


def test_complex_model():

    api = parse(Game)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/Game"}
    assert api.components == {
        "PlatformEnum": {
            "type": "string",
            "choices": ["XBOX1", "PLAYSTATION4", "PC"],
        },
        "Player": {
            "type": "object",
            "properties": {
                "nickname": {
                    "type": "string",
                    "description": "The nickname of the player over the internet",
                },
                "youtube_channel": {
                    "type": "string",
                    "description": "The YouTube channel of the player",
                },
            },
            "required": ["nickname"],
        },
        "LanguageEnum": {
            "type": "integer",
            "format": "int64",
            "choices": [1, 2, 3, 4, 5],
        },
        "CityRegionEnum": {
            "type": "string",
            "choices": ["TROPICAL", "TEMPERATE", "BOREAL"],
        },
        "City": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The city name"},
                "region": {
                    "$ref": "#/components/schemas/CityRegionEnum",
                    "description": "The region this city is located",
                },
            },
            "required": ["name"],
            "description": "One awesome city built",
        },
        "Game": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the game",
                },
                "platform": {
                    "$ref": "#/components/schemas/PlatformEnum",
                    "description": "Which platform it runs on",
                },
                "score": {
                    "type": "number",
                    "format": "double",
                    "minimum": 0,
                    "maximum": 10,
                    "multipleOf": 0.1,
                    "description": "The average score of the game",
                },
                "resolution_tested": {
                    "type": "string",
                    "pattern": "^\d+x\d+$",
                    "description": "The resolution which the game was tested",
                },
                "genre": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "uniqueItems": True,
                    "description": "One or more genres this game is part of",
                },
                "rating": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "number",
                        "format": "double",
                    },
                    "minProperties": 3,
                    "description": "Ratings given on specialized websites",
                },
                "players": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Player"},
                    "description": "Some of the notorious players of this game",
                },
                "language": {
                    "$ref": "#/components/schemas/LanguageEnum",
                    "description": "The main language of the game",
                },
                "awesome_city": {"$ref": "#/components/schemas/City"},
                "remarkable_resources": {
                    "anyOf": [
                        {"$ref": "#/components/schemas/Player"},
                        {"$ref": "#/components/schemas/City"},
                    ],
                    "description": "Some remarkable resources of this game over the internet",
                },
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
                "remarkable_resources",
            ],
            "description": "An electronic game model",
        },
    }


def test_complex_model_inline():

    with middle.config.temp(
        openapi_model_as_component=False, openapi_enum_as_component=False
    ):
        api = parse(Game)

    assert isinstance(api, OpenAPI)
    assert api.components == {}
    assert api.specification == {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The name of the game"},
            "platform": {
                "type": "string",
                "choices": ["XBOX1", "PLAYSTATION4", "PC"],
                "description": "Which platform it runs on",
            },
            "score": {
                "type": "number",
                "format": "double",
                "minimum": 0,
                "maximum": 10,
                "multipleOf": 0.1,
                "description": "The average score of the game",
            },
            "resolution_tested": {
                "type": "string",
                "pattern": "^\d+x\d+$",
                "description": "The resolution which the game was tested",
            },
            "genre": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "uniqueItems": True,
                "description": "One or more genres this game is part of",
            },
            "rating": {
                "type": "object",
                "additionalProperties": {"type": "number", "format": "double"},
                "minProperties": 3,
                "description": "Ratings given on specialized websites",
            },
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "nickname": {
                            "type": "string",
                            "description": "The nickname of the player over the internet",
                        },
                        "youtube_channel": {
                            "type": "string",
                            "description": "The YouTube channel of the player",
                        },
                    },
                    "required": ["nickname"],
                },
                "description": "Some of the notorious players of this game",
            },
            "language": {
                "type": "integer",
                "format": "int64",
                "choices": [1, 2, 3, 4, 5],
                "description": "The main language of the game",
            },
            "awesome_city": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The city name"},
                    "region": {
                        "type": "string",
                        "choices": ["TROPICAL", "TEMPERATE", "BOREAL"],
                        "description": "The region this city is located",
                    },
                },
                "required": ["name"],
                "description": "One awesome city built",
            },
            "remarkable_resources": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "nickname": {
                                "type": "string",
                                "description": "The nickname of the player over the internet",
                            },
                            "youtube_channel": {
                                "type": "string",
                                "description": "The YouTube channel of the player",
                            },
                        },
                        "required": ["nickname"],
                    },
                    {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The city name",
                            },
                            "region": {
                                "type": "string",
                                "choices": ["TROPICAL", "TEMPERATE", "BOREAL"],
                                "description": "The region this city is located",
                            },
                        },
                        "required": ["name"],
                        "description": "One awesome city built",
                    },
                ],
                "description": "Some remarkable resources of this game over the internet",
            },
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
            "remarkable_resources",
        ],
        "description": "An electronic game model",
    }

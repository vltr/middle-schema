import inspect

import middle


def snake_to_camel_case(snake_str):
    # from https://stackoverflow.com/a/42450252
    first, *others = snake_str.split("_")
    return "".join([first.lower(), *map(str.title, others)])


def is_model(model_or_field):
    return inspect.isclass(model_or_field) and issubclass(
        model_or_field, middle.Model
    )

def snake_to_camel_case(snake_str):
    # from https://stackoverflow.com/a/42450252
    first, *others = snake_str.split("_")
    return "".join([first.lower(), *map(str.title, others)])


def raise_simple_type(simple_type, *encouraged_type):
    if len(encouraged_type) > 1:
        encouraged = ", ".join([str(t.__name__) for t in encouraged_type])
    else:
        encouraged = str(encouraged_type[0])
    raise TypeError(
        'It is encouraged to use "{}" instead of "{}"'.format(
            encouraged, simple_type.__name__
        )
    )

def validate_argparser(args):
    to_exit = False
    for key in args.__dict__:
        value = args.__dict__[key]
        is_missing_value = False
        try:
            if value is None or (type(value) == str and not len(value)):
                is_missing_value = True
        except KeyError as e:
            is_missing_value = True

        if is_missing_value:
            print(f'Missing {key} parameter')
            to_exit = True

    return to_exit
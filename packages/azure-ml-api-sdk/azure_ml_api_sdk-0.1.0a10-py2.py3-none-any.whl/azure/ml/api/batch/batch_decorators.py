def add_input(name, default=None):
    def wrapper(original_function):
        __add_arg(original_function, 'inputs', name, default)

        return original_function
    return wrapper


def add_output(name, default=None):
    def wrapper(original_function):
        __add_arg(original_function, 'outputs', name, default)

        return original_function
    return wrapper


def add_parameters(name, default=None, type=str):
    def wrapper(original_function):
        __add_arg(original_function, 'parameters', name, default, type)

        return original_function

    return wrapper


def add_dependency(dependency):
    def wrapper(original_function):
        __add_arg(original_function, 'dependencies', dependency)

        return original_function

    return wrapper


def __add_arg(original_function, arg_type, name, default=None, param_type=str):
    if hasattr(original_function, '__annotations__'):
        if arg_type in original_function.__annotations__:
            original_function.__annotations__[arg_type].append(__generate_arg_info(name, default, param_type))
        else:
            original_function.__annotations__[arg_type] = [__generate_arg_info(name, default, param_type)]
    else:
        original_function.__annotations__ = {arg_type: [__generate_arg_info(name, default, param_type)]}


def __generate_arg_info(name, default, param_type):
    arg = {'name': name,
           'parser_name': name.replace('_', '-'),
           'default': default,
           'param_type': param_type}

    return arg

import inspect
import os

BATCH_DRIVER_FILE = 'service_driver.py'


def generate_driver_file(run_func):
    frame = inspect.currentframe()

    try:
        frames = inspect.getouterframes(frame)
        sdk_frame = frames[1]

        run_code = inspect.getsourcelines(run_func)

        try:
            sdk_location = os.path.dirname(os.path.dirname(sdk_frame.filename))
            main_function = generate_main(run_func.__annotations__, run_func.func_name)
        except AttributeError:
            sdk_location = os.path.dirname(os.path.dirname(sdk_frame[1]))
            main_function = generate_main(run_func.__annotations__, run_func.__name__)

        with open(BATCH_DRIVER_FILE, 'w') as service_result_file:
            # These lines are a standin until the sdk is native in the base image
            service_result_file.write('import sys\n')
            service_result_file.write('if not "{0}" in sys.path:\n    sys.path.append("{0}")\n'.format(sdk_location))
            service_result_file.write('from batch import batch_decorators\n\n')
            for line in run_code[0]:
                service_result_file.write(line)
            service_result_file.write('\n\nif __name__ == "__main__":\n')
            for line in main_function:
                service_result_file.write('    {}\n'.format(line))

        return run_func.__annotations__
    except IOError as e:
        print(e)
        return
    finally:
        del frame


def generate_main(function_annotations, function_name):
    main_function = ['import argparse', 'parser = argparse.ArgumentParser()']

    args = []

    if 'inputs' in function_annotations:
        args.extend(function_annotations['inputs'])
    if 'outputs' in function_annotations:
        args.extend(function_annotations['outputs'])
    if 'parameters' in function_annotations:
        args.extend(function_annotations['parameters'])

    for arg in args:
        main_function.append('parser.add_argument("--{}", dest="{}", type={})'.format(arg['parser_name'], arg['name'], arg['param_type'].__name__))

    main_function.append('parsed_args = parser.parse_args()')
    main_function.append('{}(**vars(parsed_args))'.format(function_name))

    return main_function


def generate_create_command(service_name, function_annotations):
    command = 'az ml service create batch -f {} -n {} '.format(BATCH_DRIVER_FILE, service_name)

    args = []

    if 'inputs' in function_annotations:
        args.extend([('in', arg) for arg in function_annotations['inputs']])
    if 'outputs' in function_annotations:
        args.extend([('out', arg) for arg in function_annotations['outputs']])
    if 'parameters' in function_annotations:
        args.extend([('param', arg) for arg in function_annotations['parameters']])

    for flag, arg in args:
        command += '--{}=--{}'.format(flag, arg['parser_name'])
        if arg['default']:
            command += ':{} '.format(arg['default'])
        else:
            command += ' '

    if 'dependencies' in function_annotations:
        for arg in function_annotations['dependencies']:
            command += '-d {} '.format(arg['name'])

    return command

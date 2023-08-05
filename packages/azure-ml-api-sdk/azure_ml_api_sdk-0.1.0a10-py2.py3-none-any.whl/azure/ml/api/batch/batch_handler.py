from azure.cli.command_modules.ml.service import batch
from ._batch_sdk_utilities import BATCH_DRIVER_FILE
from ._batch_sdk_utilities import generate_driver_file
from ._batch_sdk_utilities import generate_create_command


def prepare(run_func, service_name):
    function_annotations = generate_driver_file(run_func)
    print(generate_create_command(service_name, function_annotations))


def publish(run_func, service_name, service_title='a_title', verb=False):
    function_annotations = generate_driver_file(run_func)

    args = []
    inputs = []
    outputs = []
    parameters = []
    dependencies = []

    if 'inputs' in function_annotations:
        args.extend([(inputs, arg) for arg in function_annotations['inputs']])
    if 'outputs' in function_annotations:
        args.extend([(outputs, arg) for arg in function_annotations['outputs']])
    if 'parameters' in function_annotations:
        args.extend([(parameters, arg) for arg in function_annotations['parameters']])

    for arg_list, arg in args:
        if arg['default']:
            arg_list.append('--{}:{}'.format(arg['parser_name'], arg['default']))
        else:
            arg_list.append('--{}'.format(arg['parser_name']))

    if 'dependencies' in function_annotations:
        for arg in function_annotations['dependencies']:
            dependencies.append(arg['name'])

    batch.batch_service_create(driver_file=BATCH_DRIVER_FILE,
                               service_name=service_name,
                               title=service_title,
                               verb=verb,
                               inputs=inputs,
                               outputs=outputs,
                               parameters=parameters,
                               dependencies=dependencies)


def run(service_name, inputs, outputs, parameters, job_name=None, wait=False, verb=False):
    batch.batch_service_run(service_name=service_name,
                            inputs=inputs,
                            outputs=outputs,
                            parameters=parameters,
                            job_name=job_name,
                            wait_for_completion=wait,
                            verb=verb)


def list():
    batch.batch_service_list()


def view(service_name, verb=False):
    batch.batch_service_view(service_name, verb)


def delete(service_name, verb=False):
    batch.batch_service_delete(service_name, verb)


def list_jobs(service_name):
    batch.batch_list_jobs(service_name)


def view_job(service_name, job_name, verb=False):
    batch.batch_view_job(service_name, job_name, verb)


def cancel_job(service_name, job_name, verb=False):
    batch.batch_cancel_job(service_name, job_name, verb)

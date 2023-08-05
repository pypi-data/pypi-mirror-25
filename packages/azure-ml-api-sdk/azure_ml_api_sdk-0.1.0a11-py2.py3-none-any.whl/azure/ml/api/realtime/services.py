# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import datetime
import inspect
import os
import subprocess
import zipfile
from shutil import copyfile, copytree
from shutil import rmtree
from zipfile import ZipFile

from azure.ml.api.schema.schemautil import *

USER_RUN_FUNCTION_NAME= "user_run_method"
USER_INIT_FUNCTION_NAME = "user_init_method"
REQUIREMENTS_FOLDER_NAME = "requirements"
ATTACHED_FILES_FOLDER_NAME = "attached_files"
DRIVER_FILE_NAME = "main.py"


def get_main():
    return '''from azure.ml.api.schema.schemautil import *


<user_run_function>
<user_init_function>
def run(http_body):
    arguments = parse_service_input(http_body, aml_serialized_input_types)
    return_obj = user_run_func(**arguments)
    return return_obj


def init():
    global aml_serialized_output_type
    global aml_serialized_input_types
    aml_serialized_input_types, aml_serialized_output_type = load_service_schema("<schema_file>")
    user_init_func()
    '''


def _get_source(func):
    source = inspect.getsource(func)
    splits = source.split('\n')
    defCountered = False
    source = ""
    for split in splits:
        if not defCountered:
            if split.startswith('def'):
                defCountered = True
        else:
            source += split + '\n'
    return source


def _get_args(func):
    args = inspect.getargs(func.__code__)
    all_args = args.args
    if args.varargs is not None:
        all_args.append(args.varargs)
    if args.varkw is not None:
        all_args.append(args.keywords)
    return all_args


def _construct_run_function_signature(args):
    if len(args) > 1:
        arg_list = ", ".join(args)
    elif len(args) == 1:
        arg_list = args[0]
    else:
        arg_list=""
    return "def " + USER_RUN_FUNCTION_NAME + "(" + arg_list + "):\n"


def _get_input_pickle(input_types):
    return pickle.dumps(input_types)


def _get_output_pickle(output_type):
    return pickle.dumps(output_type)


def _process_run_func(run_func, input_types, output_type, main, schema_filename):
    run_args = _get_args(run_func)
    if len(run_args) != len(input_types):
        raise Exception(
            "Function has {0} arguments while declared inputs for run function has {1} arguments".format(len(run_args),
                                                                                                         len(input_types)))
    output_type_pickle = _get_output_pickle(output_type)
    source = _construct_run_function_signature(run_args) + _get_source(run_func)
    main = main.replace('<output_type>', str(output_type_pickle))
    main = main.replace('<schema_file>', schema_filename)
    main = main.replace('<user_run_function>', source)
    main = main.replace('user_run_func', USER_RUN_FUNCTION_NAME)
    return main


def _process_init_func(init_func, main):
    if len(_get_args(init_func)) > 0:
        raise Exception("init function cannot have arguments to it")
    init_function_signature = 'def ' + USER_INIT_FUNCTION_NAME + "():\n"
    source = init_function_signature + _get_source(init_func)
    main = main.replace('<user_init_function>', source)
    main = main.replace('user_init_func', USER_INIT_FUNCTION_NAME)
    return main


def _get_unique_time_stamp():
    return datetime.datetime.today().strftime('%Y%m%d%H%M%S')


def _create_directory(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except:
        print("Failed to create ouput directory")
        raise


def _cleanup(output_directory_name):
    try:
        if os.path.exists(output_directory_name):
            rmtree(output_directory_name)
    except:
        print("Failed cleanup")
        raise


def _create_output_directory(main, input_types, output_types,
                             schema_file_name, attached_files=None, requirements_file=None):
    output_directory_name= "output_"+_get_unique_time_stamp()
    try:
        _create_directory(output_directory_name)
        save_service_schema(input_types, output_types, os.path.join(output_directory_name, schema_file_name))
        _save_main_file(main, output_directory_name)
        if attached_files is not None:
            _copy_attached_files(attached_files, output_directory_name)

        if requirements_file is not None:
            _copy_requirements_file(requirements_file, output_directory_name)
        return output_directory_name
    except:
        _cleanup(output_directory_name)
        print("Failed to create output directory")
        raise
    return output_directory_name


def _copy_file(source, destination):
    try:
        copyfile(source, os.path.join(destination, os.path.basename(source)))
    except:
        print("Error copying file: {0}".format(source))
        raise


def _copy_directory(source, destination):
    try:
        copytree(source, os.path.join(destination, os.path.basename(source)))
    except:
        print("Failed to copy directory: {0}".format(source))
        raise


def _copy_attached_files(attached_files, output_directory):
    destination = os.path.join(output_directory, ATTACHED_FILES_FOLDER_NAME)
    _create_directory(destination)
    print("copying over attached files to output directory")
    for file in attached_files:
        print("copying file {0}".format(file))
        if os.path.isdir(file):
            _copy_directory(file, destination)
        else:
            _copy_file(file, destination)


def _copy_requirements_file(requirements_file, output_directory):
    destination = os.path.join(output_directory, REQUIREMENTS_FOLDER_NAME)
    _create_directory(destination)
    try:
        print("copying requirements file: {0}".format(requirements_file))
        copyfile(requirements_file, os.path.join(destination,'requirements.txt'))
    except:
        print("Requirements file {0} could not be copied".format(requirements_file))
        raise


def _save_main_file(main, directory_name):
    try:
        with open(os.path.join(directory_name, DRIVER_FILE_NAME), "w") as py_file:
            py_file.write(main)
    except:
        print("Failed to create {0} file".format(DRIVER_FILE_NAME))
        raise


def _create_output_zip(main, attached_files=None, pipFile=None):
    zipfile_name = 'output_' + _get_unique_time_stamp() + '.zip'
    with ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        try:
            myzip.writestr('main.py', main)
        except:
            print("Failed to write main.py to zipfile")
            raise

        if pipFile is not None:
            try:
                myzip.write(pipFile, os.path.join('requirements',pipFile))
            except:
                print("Failed to write requirements.txt file to zipfile")
                raise

        if attached_files is not None:
            for file in attached_files:
                try:
                    myzip.write(file, os.path.join('attached_files', file))
                except:
                    print("Failed to write file {0} to zipfile".format(file))
                    raise
    print("Output zipfile {0} has been created".format(zipfile_name))


def _do_publish_local(webservice_name, output_directory_location, runtime, ice_endpoint="http://52.184.190.21/"):
    main = os.path.join(output_directory_location, DRIVER_FILE_NAME)
    attached_files_path = os.path.join(output_directory_location, ATTACHED_FILES_FOLDER_NAME)
    requirements_path = os.path.join(output_directory_location, REQUIREMENTS_FOLDER_NAME)
    cli__invoke_string =  "az ml service create realtime -n  {0} -f {1} -r {2} -i {3}".format(webservice_name, main, runtime, ice_endpoint)
    if os.path.exists(attached_files_path):
        cli__invoke_string += " -d {0}".format(attached_files_path)
    if os.path.exists(requirements_path):
        cli__invoke_string += " -p {0}".format(os.path.join(requirements_path, "requirements.txt"))
    try:
        subprocess.check_call([cli__invoke_string], shell=True)
    except Exception as e:
        print("Calling CLI failed")
        raise e
    _cleanup(output_directory_location)


def prepare(run_func, init_func, input_types, output_type, runtime, attached_files=None, pip_requirements_file_location=None):
    if runtime is None:
        raise Exception("RunTime needs to be specified")
    if run_func is None:
        raise Exception("run function needs to be specified and cannot be None")
    if init_func is None:
        raise Exception("init function needs to be specified and cannot be None")
    main = get_main()
    print("processing init function")
    main = _process_init_func(init_func, main)
    print("processing inputs")
    schema_file_name = "input_types_{0}.json".format(_get_unique_time_stamp())
    print("processing run function")
    main = _process_run_func(run_func, input_types, output_type, main, schema_file_name)
    print("setting up output directory")
    output_dir = _create_output_directory(main, input_types, output_type, schema_file_name, attached_files,
                                    pip_requirements_file_location)
    print("Done setting up output directory, available here {0}".format(output_dir))
    return output_dir


def publish(webservice_name, run_func, init_func, input_types, output_type, runtime, attached_files=None,
            pip_requirements_file_location=None, acr_credentials=None, deploy_local=True, acs_credentials=None,
            logging_settings=None, ice_endpoint=None):
    print("Starting publish")
    output_directory = None
    try:
        output_directory = prepare(run_func, init_func, input_types, output_type, runtime, attached_files,
                                   pip_requirements_file_location)
    except:
        print("Error creating driver program and setting up files")
        raise
    _do_publish_local(webservice_name, output_directory, runtime)
    print("publish done")
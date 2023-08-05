# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Utilities to save and load heteregenous schema and type dictionary, also used to parse http input using the schema and
type dictionary
"""
import pickle
import base64
import json
import os.path
from azure.ml.api.schema.sampleDefinition import SampleDefinition
from azure.ml.api.exceptions.BadRequest import BadRequestException
from azure.ml.api.exceptions.InternalServerError import InternalServerException
from azure.ml.api.schema.schemaObjects import Schema
from azure.ml.api.schema.dataTypes import DataTypes


def _serialize_to_string(obj):
    serialized_bytes = pickle.dumps(obj)
    b64encoded_bytes = base64.b64encode(serialized_bytes)
    return b64encoded_bytes.decode('utf-8')


def _deserialize_from_string(obj):
    bytes = base64.b64decode(obj.encode('utf-8'))
    return pickle.loads(bytes)


def _get_serialized_schema_dict(schema):
    if schema is None:
        return
    result = dict()
    for input_key, input_value in schema.items():
        if isinstance(input_value, SampleDefinition):
            result[input_key] = input_value.serialize()
        elif isinstance(input_value, type):
            # swagger is empty here will need to add in generation code for types
            result[input_key] = {
                "internal": _serialize_to_string(input_value),
                "swagger": ""
            }
        else:
            raise ValueError("Invalid Schema: Bad input type detected for argument {0}, "
                             "input schema only supports types or Sample Definition objects, "
                             "found {1}".format(input_key, type(input_value)))
    return result


def _get_deserialized_schema_dict(schema):
    result = dict()
    for input_key, input_value in schema.items():
        if "internal" not in input_value or input_value["internal"] is None:
            raise ValueError("Invalid schema, internal schema not found for item {0}".format(input_key))
        if "swagger" not in input_value or input_value["swagger"] is None:
            raise ValueError("Invalid schema, swagger not found for item {0}".format(input_key))

        data_type = None
        if "type" in input_value:
            data_type = input_value["type"]
        if data_type is not None:
            internal_schema = _get_internal_schema(data_type, input_value["internal"])
            result[input_key] = Schema(data_type, internal_schema, input_value["swagger"])
        else:
            data_type = _deserialize_from_string(input_value["internal"])
            if not isinstance(data_type, type):
                raise ValueError("Invalid schema, type of internal object "
                                 "should either be SchemaObject or an instance of "
                                 "type, found {0} of key {1}".format(type(data_type), input_key))
            result[input_key] = data_type
    return result


def _get_internal_schema(data_type, schema_string):
    if data_type is DataTypes.NUMPY:
        from azure.ml.api.schema.numpyutil import NumpySchema
        return NumpySchema.deserialize_from_string(schema_string)
    elif data_type is DataTypes.SPARK:
        from azure.ml.api.schema.sparkutil import SparkSchema
        return SparkSchema.deserialize_from_string(schema_string)
    elif data_type is DataTypes.PANDAS:
        from azure.ml.api.schema.pandasutil import PandasSchema
        return PandasSchema.deserialize_from_string(schema_string)


def _get_complex_datatype(arg_key, arg_value, schema):
    try:
        if not isinstance(arg_value, list):
            raise ValueError("Invalid input format: expected an array.")
        if schema.type is DataTypes.NUMPY:
            from azure.ml.api.schema.numpyutil import NumpyUtil
            return NumpyUtil.get_input_object(arg_value, schema)
        elif schema.type is DataTypes.SPARK:
            from azure.ml.api.schema.sparkutil import SparkUtil
            return SparkUtil.get_input_object(arg_value, schema)
        elif schema.type is DataTypes.PANDAS:
            from azure.ml.api.schema.pandasutil import PandasUtil
            return PandasUtil.get_input_object(arg_value, schema)
    except ValueError as ex:
        raise BadRequestException("Failed to deserialize {0} to type provided by input schema, Error Details: {1}"
                                  .format(arg_key, str(ex)))


def save_service_schema(file_path, input_schema_sample = None, output_schema_sample = None):
    if file_path is None or len(file_path) == 0:
        raise ValueError("A file path for the schema must be specified")
    target_dir = os.path.dirname(file_path)
    if len(target_dir) > 0 and not os.path.exists(target_dir):
        raise ValueError("Please specify a valid path to save the schema file to")
    if input_schema_sample is None and output_schema_sample is None:
        raise ValueError("At least one of the input / output schema samples need to be specified on this call")

    result_dict = dict()
    if input_schema_sample is not None:
        if not isinstance(input_schema_sample, dict):
            raise ValueError("Invalid input schema sample: must be a map input name -> input definition")
        result_dict["input"] = _get_serialized_schema_dict(input_schema_sample)
    if output_schema_sample is not None:
        if not isinstance(output_schema_sample, dict):
            raise ValueError("Invalid output schema sample: must be a map output name -> output definition")
        result_dict["output"] = _get_serialized_schema_dict(output_schema_sample)

    try:
        with open(file_path, 'w') as outfile:
            json.dump(result_dict, outfile)
    except:
        print("Failed to save schema file")
        raise


def parse_service_input(http_body, input_schema):
    input_json = json.loads(http_body)
    run_input = dict()
    if type(input_json) != dict:
        raise BadRequestException("Input request is not in format as specified by swagger")
    if set(input_schema.keys()) != set(input_json.keys()):
        raise BadRequestException("Argument mismatch: Provided inputs ({0}) while run function has inputs ({1})"
                                  .format(", ".join(input_json.keys()), ",".join(input_schema)))
    for arg_key, arg_value in input_json.items():
        if type(input_schema[arg_key]) == type:
            # dealing with non-complex data types here
            if input_schema[arg_key] != type(arg_value):
                raise BadRequestException("Input type mismatch: {0} is of type {1} should be of type {2}"
                                          .format(arg_key, type(arg_value), input_schema[arg_key]))
            run_input[arg_key] = arg_value
        elif isinstance(input_schema[arg_key], Schema):
            # dealing with a complex type here
            run_input[arg_key] = _get_complex_datatype(arg_key, arg_value, input_schema[arg_key])
        else:
            raise InternalServerException("Bad input type detected: {0}".format(type(input_schema[arg_key])))
    return run_input


def load_service_schema(filename):
    if filename is None:
        raise TypeError('A filename must be specified.')
    if not os.path.exists(filename):
        raise ValueError('Specified schema file cannot be found: {}.'.format(filename))
    with open(filename, 'r') as outfile:
        schema_document = json.load(outfile)

    input_schema = None
    if "input" in schema_document:
        input_schema = _get_deserialized_schema_dict(schema_document["input"])
    output_schema = None
    if "output" in schema_document:
        output_schema = _get_deserialized_schema_dict(schema_document["output"])
    return input_schema, output_schema

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Utilities to save and load schema information for Numpy Arrays.
"""

import numpy as np
import pickle
import base64
from azure.ml.api.schema.common import BaseUtil, SwaggerUtil
from azure.ml.api.schema.schemaObjects import Schema, InternalSchema
from azure.ml.api.schema.dataTypes import DataTypes
from azure.ml.api.schema.dtypeToSwagger import Dtype2Swagger


class NumpySchema(InternalSchema):

    def __init__(self, shape, data_type):
        if not isinstance(shape, tuple):
            raise TypeError("Invalid shape parameter: must be a tuple with array dimensions")
        if not isinstance(data_type, np.dtype):
            raise TypeError("Invalid data_type parameter: must be a valid numpy.dtype")
        self.shape = shape
        self.data_type = data_type

    def serialize_to_string(self):
        serialized_bytes = pickle.dumps(self)
        b64encoded_bytes = base64.b64encode(serialized_bytes)
        return b64encoded_bytes.decode('utf-8')

    @classmethod
    def deserialize_from_string(cls, serialized_schema_string):
        schema_bytes = base64.b64decode(serialized_schema_string.encode('utf-8'))
        return pickle.loads(schema_bytes)


class NumpyUtil(BaseUtil):
    type = DataTypes.NUMPY

    @classmethod
    def extract_schema(cls, array):
        if not isinstance(array, np.ndarray):
            raise TypeError('Only valid numpy array can be passed in to extract schema from.')
        schema = NumpySchema(array.shape, array.dtype)

        # Create the swagger schema for the data type of the array
        swagger_item_type = Dtype2Swagger.convert_dtype_to_swagger(schema.data_type)
        swagger_schema = Dtype2Swagger.handle_swagger_array(swagger_item_type, schema.shape)

        # Also extract some sample values for the schema from the first few items of the array
        items_count = min(len(array), BaseUtil._MAX_RECORDS_FOR_SAMPLE_SCHEMA)
        swagger_schema['example'] = SwaggerUtil.get_swagger_sample(array, items_count, swagger_item_type)

        return Schema(NumpyUtil.type, schema, swagger_schema)

    @classmethod
    def get_input_object(cls, parsed_input, schema):
        for i in range(len(parsed_input)):
            parsed_input[i] = NumpyUtil._numpify_json_object(parsed_input[i], schema.internal.data_type)
        numpy_array = np.array(object=parsed_input, dtype=schema.internal.data_type, copy=False)

        # Validate the schema of the parsed data against the known one
        expected_shape = schema.internal.shape
        parsed_dims = len(numpy_array.shape)
        expected_dims = len(expected_shape)
        if parsed_dims != expected_dims:
            raise ValueError(
                "Invalid input array: an array with {0} dimensions is expected; "
                "input has {1} [shape {2}]".format(expected_dims, parsed_dims, numpy_array.shape))
        for dim in range(1, len(expected_shape)):
            if numpy_array.shape[dim] != expected_shape[dim]:
                raise ValueError(
                    'Invalid input array: array has size {0} on dimension #{1}, '
                    'while expected value is {2}'.format(numpy_array.shape[dim], dim, expected_shape[dim]))

        return numpy_array

    @classmethod
    def _load_internal_schema_object(cls, serialized_internal_schema):
        internal_schema = NumpySchema.deserialize_from_string(serialized_internal_schema)
        if internal_schema.data_type is None:
            raise ValueError("Invalid array schema: the data_type property must be specified")
        if internal_schema.shape is None:
            raise ValueError("Invalid array schema: the shape property must be specified")

        return internal_schema

    @staticmethod
    def _numpify_json_object(item, item_dtype):
        if len(item_dtype) > 0:
            converted_item = []
            for field_name in item_dtype.names:
                new_item_field = NumpyUtil._numpify_json_object(item[field_name], item_dtype[field_name])
                converted_item.append(new_item_field)
            return tuple(converted_item)
        else:
            return item

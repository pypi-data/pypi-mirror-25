# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import abc
from azure.ml.api.schema.dataTypes import DataTypes


class InternalSchema(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def serialize_to_string(self):
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize_from_string(cls):
        pass


class Schema(object):
    def __init__(self, data_type, internal_form, swagger_form):
        if not isinstance(internal_form, InternalSchema):
            raise TypeError("Internal schema parameter must be specified as an instance of InternalSchema.")
        if not isinstance(swagger_form, dict):
            raise TypeError("Swagger schema parameter must be specified as a dict instance.")
        self.type = data_type
        self.internal = internal_form
        self.swagger = swagger_form


class ServiceSchema(object):
    def __init__(self, input_schema, output_schema):
        if input_schema and not isinstance(input_schema, Schema):
            raise TypeError("Invalid input schema parameter: must be an instance of the Schema class")
        if output_schema and not isinstance(output_schema, Schema):
            raise TypeError("Invalid input schema parameter: must be an instance of the Schema class")
        self.input = input_schema
        self.output = output_schema

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.ml.api.schema.dataTypes import DataTypes


class SampleDefinition:
    def __init__(self, input_type, sample_data):
        if not isinstance(input_type, int):
            raise Exception("Argument input_type needs to be of data DataTypes")
        self.type = input_type
        self.schema = self._get_schema(sample_data)

    def _get_schema(self, sample_data):
        if self.type is DataTypes.NUMPY:
            from azure.ml.api.schema.numpyutil import NumpyUtil
            return NumpyUtil.extract_schema(sample_data)
        elif self.type is DataTypes.SPARK:
            from azure.ml.api.schema.sparkutil import SparkUtil
            return SparkUtil.extract_schema(sample_data)
        elif self.type is DataTypes.PANDAS:
            from azure.ml.api.schema.pandasutil import PandasUtil
            return PandasUtil.extract_schema(sample_data)

    def serialize(self):
        return {"internal": self.get_schema_string(), "swagger": self.schema.swagger, "type": self.type}

    def get_schema_string(self):
        return self.schema.internal.serialize_to_string()


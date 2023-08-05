# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Utilities to save and load schema information for Spark DataFrames.
"""

from pyspark.sql import SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *
from azure.ml.api.schema.common import BaseUtil, SwaggerUtil
from azure.ml.api.schema.schemaObjects import Schema, InternalSchema
from azure.ml.api.schema.dataTypes import DataTypes
from azure.ml.api.schema.sparkToSwagger import Spark2Swagger
from azure.ml.api.schema.dtypeToSwagger import Dtype2Swagger


class SparkSchema(InternalSchema):

    def __init__(self, df_schema):
        if not isinstance(df_schema, StructType):
            raise TypeError("Invalid data fme schema parameter: must be a valid StructType object")
        self.schema = df_schema

    def serialize_to_string(self):
        return self.schema.jsonValue()

    @classmethod
    def deserialize_from_string(cls, serialized_schema_string):
        df_schema = StructType.fromJson(serialized_schema_string)
        return SparkSchema(df_schema)


class SparkUtil(BaseUtil):
    type = DataTypes.SPARK

    spark_session = SparkSession.builder.getOrCreate()
    sqlContext = SQLContext(spark_session.sparkContext)

    @classmethod
    def extract_schema(cls, data_frame):
        if not isinstance(data_frame, DataFrame):
            raise TypeError('Invalid data type: expected a Spark data frame.')

        internal_schema = SparkSchema(data_frame.schema)
        swagger_schema = Spark2Swagger.convert_spark_dataframe_schema_to_swagger(data_frame.schema)

        # Also extract some sample values for the schema from the first few items of the array
        items_to_sample = data_frame.take(BaseUtil._MAX_RECORDS_FOR_SAMPLE_SCHEMA)
        items_count = len(items_to_sample)
        df_record_swagger = swagger_schema['items']
        swagger_schema['example'] = SwaggerUtil.get_swagger_sample(items_to_sample, items_count, df_record_swagger)

        return Schema(SparkUtil.type, internal_schema, swagger_schema)

    @classmethod
    def get_input_object(cls, input_data, schema):
        data_frame = SparkUtil.sqlContext.createDataFrame(data=input_data, schema=schema.internal.schema,
                                                          verifySchema=True)
        return data_frame

    @classmethod
    def _load_internal_schema_object(cls, serialized_internal_schema):
        internal_schema = SparkSchema.deserialize_from_string(serialized_internal_schema)
        return internal_schema

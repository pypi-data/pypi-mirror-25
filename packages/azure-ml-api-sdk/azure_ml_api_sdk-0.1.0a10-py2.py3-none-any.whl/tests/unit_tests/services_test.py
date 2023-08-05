# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest
import shutil

import numpy as np

from azure.ml.api.realtime.services import prepare
from azure.ml.api.schema.sampleDefinition import SampleDefinition
from azure.ml.api.schema.dataTypes import DataTypes


class Servicestest(unittest.TestCase):
    tests_folder = os.path.dirname(os.path.abspath(__file__))

    def test_service_happy_path(self):
        int_array = np.array(range(10), dtype=np.int32)
        input_types = {'a': SampleDefinition(DataTypes.NUMPY, int_array), 'b':int}
        output_types ={'output1':str}
        output_folder = prepare(sample_run, sample_init, input_types, output_types, "scikit")
        output_path= os.path.join(Servicestest.tests_folder, output_folder)
        if not os.path.exists(output_path):
            self.fail("output folder not created")
        if not os.path.exists(os.path.join(output_path, "main.py")):
            self.fail("output folder does not have main.py")
        shutil.rmtree(output_path)


def sample_init():
    pass


def sample_run(a, b):
    print(a)
    return b

import pandas as pd
from typing import List

from .clean_list import clean_numbers
from .clean_value import number_cleaner
from primitive_interfaces.base import PrimitiveBase

Inputs = pd.DataFrame
Outputs = pd.DataFrame
Params = dict
CallMetadata = dict

class CleanNumbers(PrimitiveBase[Inputs, Outputs, Params]):
    __author__ = 'distil'
    __metadata__ = {
        "id": "d4582270-bc46-346a-9925-7bfc3e8d2bfc",
        "name": "punk.preppy.cleanNumbers.CleanNumbers",
        "common_name": "CleanNumbers",
        "description": "Forcing just about anything that looks like a number into a float",
        "languages": [
            "python3.6"
        ],
        "library": "punk",
        "version": "1.1.1",
        "source_code": "https://github.com/NewKnowledge/punk/blob/dev/punk/preppy/cleanNumbers.py",
        "is_class": True,
        "interface_type": "data_cleaning",
        "algorithm_type": [                                                         
            "data_preparation"                                              
        ],
        "task_type": [
            "data cleaning"                                              
        ],
        "output_type": [
            "features"
        ], 
        "team": "distil",
        "schema_version": 1.0,
        "build": [
            {
                "type": "pip",
                "package": "punk"
            }
        ],
        "compute_resources": {
            "sample_size": [
                1000.0, 
                10.0
            ],
            "sample_unit": [
                "MB"
            ],
            "num_nodes": [
                1
            ],
            "cores_per_node": [
                1
            ],
            "gpus_per_node": [
                0
            ],
            "mem_per_node": [
                1.0
            ],
            "disk_per_node": [
                1.0
            ],
            "mem_per_gpu": [
                0.0
            ],
            "expected_running_time": [
                5.0
            ]
        }
    }

    def __init__(self):
        pass

    def get_params(self) -> Params:
        return {}

    def set_params(self, params: Params) -> None:
        self.params = params

    def get_call_metadata(self) -> CallMetadata: 
        return {}

    def fit(self) -> None:
        pass

    def produce(self, inputs: Inputs) -> Outputs:
        return inputs.apply(clean_numbers)
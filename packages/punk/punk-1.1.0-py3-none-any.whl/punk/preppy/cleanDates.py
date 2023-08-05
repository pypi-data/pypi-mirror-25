import pandas as pd
from typing import List
from datetime import datetime

from .clean_list import clean_dates
from primitive_interfaces.base import PrimitiveBase

Inputs = pd.DataFrame
Outputs = List[datetime]
Params = dict
CallMetadata = dict


class CleanDates(PrimitiveBase[Inputs, Outputs, Params]):
    __author__ = 'distil'
    __metadata__ = {
        "id": "8a2fe029-6817-35f6-8822-2674910d9e8f",
        "name": "punk.preppy.cleanDates.CleanDates",
        "common_name": "CleanDates",
        "description": "Forcing just about anything that looks like a datetime string into a datetime object",
        "languages": [
            "python3.6"
        ],
        "library": "punk",
        "version": "1.1.0",
        "source_code": "https://github.com/NewKnowledge/punk/blob/dev/punk/preppy/cleanDates.py",
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

    def transform(self, inputs: Inputs) -> Outputs:
        return [clean_dates(l) for l in inputs]
import numpy as np
from sklearn.decomposition import PCA
from typing import NamedTuple, List
from primitive_interfaces.base import PrimitiveBase

Input = np.ndarray
Output = List[int]
Params = dict
CallMetadata = dict

class PCAFeatures(PrimitiveBase[Input, Output, Params]):
    __author__ = "distil"
    __metadata__ = {
        "id": "142c4056-ccd3-3530-9fcc-e9fa7052662f",
        "name": "punk.feature_selection.pca.PCAFeatures",
        "common_name": "PCAFeatures",
        "description": "Ranking of features using principal component analysis. Returns a ranking of the features based on the magnitude of their contributions to the first principal componenet and a ranking of the features based on the highest magnitude contribution to all the principal componenets.",
        "languages": [
            "python3.6"
        ],
        "library": "punk",
        "version": "1.1.1",
        "source_code": "https://github.com/NewKnowledge/punk/blob/dev/punk/feature_selection/pca.py",
        "algorithm_type": [                                                         
            "dimensionality reduction"                                              
        ],
        "task_type": [
            "feature extraction"
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


    def __init__(self) -> None:
        self.callMetadata = {}
        self.params = {}
        pass

    def fit(self) -> None:
        pass

    def get_params(self) -> Params:
        return self.params

    def set_params(self, params: Params) -> None:
        self.params = params

    def get_call_metadata(self) -> CallMetadata:
        return self.callMetadata

    def produce(self, inputs: Input) -> Output:
        """ Perform PCA and return a list of the indices of the most important
        features, ordered by contribution to first PCA component
                                                                                
        The matrix M will correspond to the absolute value of the components of 
        the decomposiiton thus giving a matrix where each column corresponds to 
        a principal component and rows are the components that rescale each 
        feature.  
                                                                                
        For example, pca.components_.T could look like this:                        
                                                                                
        array([[ 0.52237162,  0.37231836, -0.72101681, -0.26199559],                
            [-0.26335492,  0.92555649,  0.24203288,  0.12413481],                 
            [ 0.58125401,  0.02109478,  0.14089226,  0.80115427],                 
            [ 0.56561105,  0.06541577,  0.6338014 , -0.52354627]])                
                                                                                
        So the most important feature with respect to the first principal 
        component would be the 3rd feature as this has an absolute value of 
        0.58125401 which is greater than all the entries in that column.                             
                                                                                
                                                                                
        "importance_on1stpc" corresponds to the indices of most important       
        features for the first principal. Component are in ascending order      
        (most important feature 0, least important feature n_features-1).       
                                                                                
        
        Params 
        ------- 
        data : np.ndarray, [n_samples, n_features]
            Training data.
        """

        pca = PCA()

        try:
            pca.fit_transform(inputs)

            M = np.absolute(pca.components_.T)

            # Rank features based on contribtuions to 1st PC
            self.importance_on1stpc = np.argsort(M[:,0], axis=0)[::-1]
        except:
            # If any error occurs, just return indices in original order
            # In the future we should consider a better error handling strategy
            self.importance_on1stpc = [i for i in range(inputs.shape[0])]

        return self.importance_on1stpc
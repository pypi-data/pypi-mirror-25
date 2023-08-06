import numpy as np
from typing import Tuple
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.model_selection import cross_val_score
from primitive_interfaces.base import PrimitiveBase

Inputs = np.ndarray
Outputs = Tuple[Tuple[float, int], Tuple[float, int]]
Params = dict
CallMetadata = dict

class HeteroscedasticityTest(PrimitiveBase[Inputs, Outputs, Params]):
    __author__ = 'distil'
    __metadata__ = {
        "id": "25a459ea-a219-37ba-a471-b2e6a5ddd5b8",
        "name": "punk.novelty_detection.heteroscedasticity.HeteroscedasticityTest",
        "common_name": "HeteroscedasticityTest",
        "description": "Test heteroscedaticity and optimal principal subspace of data.",
        "languages": [
            "python3.6"
        ],
        "library": "punk",
        "version": "1.1.1",
        "source_code": "https://github.com/NewKnowledge/punk/blob/dev/punk/novelty_detection/heteroscedasticity.py",

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
        "interface_type" : "data_cleaning",
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

    __test__ = False

    def __init__(self, max_iter: int = 1000000, tol: int = 1e-8):
        self.max_iter = max_iter
        self.tol      = tol
        self.params = {'max_iter': self.max_iter, 'tol': self.tol}
        self.callMetadata = {}

    def fit(self) -> None:
        pass

    def get_params(self) -> Params:
        return self.params

    def set_params(self, params: Params) -> None:
        self.params = params

    def get_call_metadata(self) -> CallMetadata:
        return self.callMetadata

    def produce(self, inputs: Inputs) -> Outputs:
        """ Test heteroscedaticity of your data.

        The consequence is that the likelihood of new data can be used for 
        model selection and covariance estimation.

        Code taken from 'http://scikit-learn.org/stable/auto_examples/'             
        'decomposition/plot_pca_vs_fa_model_selection.html'.                        

        Params
        ------  
        data : array-like
            Training data.

        Returns
        -------
        "pca" returns a two tuple of number of componenets and likelihood for 
        best principal componenets estimator.                                   
        "fa" returns a two tuple of number of componenets and likelihood for 
        best factor analysis estimator.
        """
        pca = PCA(svd_solver='full')                                                
        fa = FactorAnalysis(max_iter=self.max_iter, tol=self.tol)                             

        X = inputs

        pca_scores, fa_scores = [], []                                              
        n_featues = X.shape[1]                                                      
        if n_featues > 20:                                                          
            n_components = np.arange(0, n_featues+1, 5)                             
        else:                                                                       
            n_components = np.arange(0, n_featues+1)                                
                                                                                
        for n in n_components:                                                      
            pca.n_components = n                                                    
            fa.n_components = n                                                     
            pca_scores.append( (np.mean(cross_val_score(pca, X)), n) )              
            fa_scores.append( (np.mean(cross_val_score(fa, X)), n) )                

        self.pca = max(pca_scores, key=lambda s: s[0])
        self.fa  = max(fa_scores, key=lambda s: s[0])

        return (self.pca, self.fa)
from typing import List, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline                                                                
from sklearn.model_selection import GridSearchCV
from primitive_interfaces.base import PrimitiveBase 

Inputs = Tuple[np.ndarray, np.ndarray]
Outputs = List[int]
Params = dict
CallMetadata = dict


class RFFeatures(PrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "distil"
    __metadata__ = {
        "id": "fa654741-8ab9-39ec-a9a7-3d41aaf67932",
        "name": "punk.feature_selection.rf.RFFeatures",
        "common_name": "RFFeatures",
        "description": "Ranking of features using Random Forest.",
        "languages": [
            "python3.6"
        ],
        "library": "punk",
        "version": "1.1.1",
        "source_code": "https://github.com/NewKnowledge/punk/blob/dev/punk/feature_selection/rf.py",
        "algorithm_type": [                                                         
            "decision tree"                                              
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

    def __init__(self, problem_type: str = 'classification', scoring: str ='accuracy',
                crossval: int =3, verbose: int = 0, n_jobs: int = 1):
        """
        Params
        ------
        problem_type : str
            ``classification`` or ``regression``.
        
        scoring : string, callable, list/tuple, dict or None, default: None
            A single string (see The scoring parameter: defining model
            evaluation rules) or a callable (see Defining your scoring strategy
            from metric functions) to evaluate the predictions on the test set.

            For evaluating multiple metrics, either give a list of (unique)
            strings or a dict with names as keys and callables as values.

            NOTE that when using custom scorers, each scorer should return a
            single value. Metric functions returning a list/array of values can
            be wrapped into multiple scorers that return one value each.
            
            See Specifying multiple metrics for evaluation for an example.
            
            If None, the estimator’s default scorer (if available) is used.


        crossval : int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy. Possible inputs
            for cv are:
                None, to use the default 3-fold cross validation,
                integer, to specify the number of folds in a (Stratified)KFold,
                An object to be used as a cross-validation generator.
                An iterable yielding train, test splits.

            For integer/None inputs, if the estimator is a classifier and y is
            either binary or multiclass, StratifiedKFold is used. In all other
            cases, KFold is used.

            Refer User Guide for the various cross-validation strategies that
            can be used here.

        n_jobs : int, default=1
            Number of jobs to run in parallel.

        verbose : integer
            Controls the verbosity: the higher, the more messages.
        """
        self.problem_type = problem_type
        self.crossval      = crossval
        self.scoring = scoring
        self.n_jobs  = n_jobs
        self.verbose = verbose
        self.params  = {'problem_type': self.problem_type, 'cross_validation': self.crossval,
                        'scoring': self.scoring}
        self.callMetadata = {}

    def get_params(self) -> Params:
        return self.params

    def set_params(self, params: Params) -> None:
        self.params = params

    def get_call_metadata(self) -> CallMetadata:
        return self.callMetadata

    def fit(self) -> None:
        return

    def produce(self, inputs: Inputs) -> Outputs:
        """ Rank features using Random Forest classifier.                           
                                                                                
	    Use GridSearchCV to optimize the scoring method for a random forest         
    	classifier and return the importance of the features.    

        "indices" indicate the feature importances of features order in
        ascending order (most importance feature to least important features).

        "feature_importances" The feature importances (the higher, the more
        important the feature).
                                                                                
    	Params                                                                      
    	------                                                                      
        data : tuple of arrays 
            ([n_samples, n_features], [n_samples, n_features]) corresponding to
            training data and labels.
        """
        self.X, self.y = inputs

        # Chose classfier or regressor
        if self.problem_type=="classification":
            rf = Pipeline([('clf', RandomForestClassifier(random_state=1))])    
        elif self.problem_type=="regression":
            rf = Pipeline([('clf', RandomForestRegressor(random_state=1))])
        else:
            raise ValueError(
                "problem_type must be 'classification' or 'regression'."
            )

        # Gridsearch for hyperparam optimization
        param_grid = [{'clf__n_estimators': [10, 100, 1000, 10000]},]                                          
        gs_rf = GridSearchCV(rf,                                                    
                             param_grid, 
                             cv      = self.crossval,
                             scoring = self.scoring,                                     
                             verbose = self.verbose,                                           
                             n_jobs  = self.n_jobs)                                           
        gs_rf.fit(self.X, self.y)                                                             
                                                                                
        # Rank from most to least important features (0, d-1)                       
        self.feature_importances = \
                gs_rf.best_estimator_.named_steps["clf"].feature_importances_
        self.indices = np.argsort(self.feature_importances)[::-1]                         

        return self.indices

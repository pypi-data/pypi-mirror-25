import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline                                                                
from sklearn.model_selection import GridSearchCV
from ..base import DataCleaningPrimitiveBase


class RFFeatures(DataCleaningPrimitiveBase):

    def __init__(self, problem_type, scoring, cv=3, verbose=0, n_jobs=1):
        """
        Params
        ------
        problem_type : str
            ``classification`` or ``regression``.

        cv : int, cross-validation generator or an iterable, optional
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

        verbose : integer
            Controls the verbosity: the higher, the more messages.
        """
        self.problem_type = problem_type
        self.scoring = scoring
        self.cv      = cv
        self.n_jobs  = n_jobs
        self.verbose = verbose


    def fit(self, intype, data):
        """ Rank features using Random Forest classifier.                           
                                                                                
	Use GridSearchCV to optimize the scoring method for a random forest         
    	classifier and return the importance of the features.    

        "indices" indicate the feature importances of features order in
        ascending order (most importance feature to least important features).

        "feature_importances" The feature importances (the higher, the more
        important the feature).
                                                                                
    	Params                                                                      
    	------                                                                      
        intype : list or tuple
            Expects ["matrix", "matrix"]
        data : tuple of arrays 
            ([n_samples, n_features], [n_samples, n_features]) corresponding to
            training data and labels.
        """
        # Check data format
        if isinstance(intype, (list, tuple)):
            assert(intype[0]=="matrix")
            assert(intype[1]=="matrix")
        else:
            raise ValueError("Fit expected Two 'matrix's as intype.")
        
        # Unpack data
        X, y = data

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
                             cv      = self.cv,
                             scoring = self.scoring,                                     
                             verbose = self.verbose,                                           
                             n_jobs  = self.n_jobs)                                           
        gs_rf.fit(X, y)                                                             
                                                                                
        # Rank from most to least important features (0, d-1)                       
        self.feature_importances = \
                gs_rf.best_estimator_.named_steps["clf"].feature_importances_
        self.indices = np.argsort(self.feature_importances)[::-1]                         

        return self


    def transform(self, data=None):
        return self.indices

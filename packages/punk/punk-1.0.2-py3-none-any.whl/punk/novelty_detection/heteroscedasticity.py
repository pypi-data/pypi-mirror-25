import numpy as np
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.model_selection import cross_val_score
from ..base import DataCleaningPrimitiveBase


class HeteroscedasticityTest(DataCleaningPrimitiveBase):
    __test__ = False

    def __init__(self, max_iter=1000000, tol=1e-8):
        self.max_iter = max_iter
        self.tol      = tol


    def fit(self, intype, data):
        """ Test heteroscedaticity of your data.

        The consequence is that the likelihood of new data can be used for 
        model selection and covariance estimation.

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
        if isinstance(intype, (list, tuple)):
            assert(intype[0]=="matrix")                   
        else:                                                                   
            raise ValueError("Fit expected a 'matrix' as intype.")

        self.pca_scores, self.fa_scores = self.compute_scores(data, self.max_iter, self.tol)

        self.pca = max(self.pca_scores, key=lambda s: s[0])
        self.fa  = max(self.fa_scores, key=lambda s: s[0])

        return self


    def compute_scores(self, X, max_iter=1000000, tol=1e-6):                              
        """ Compare PCA against FactorAnalysis.                                     
                                                                                
        Code taken from 'http://scikit-learn.org/stable/auto_examples/'             
        'decomposition/plot_pca_vs_fa_model_selection.html'.                        
                                                                                
        Params                                                                      
        ------                                                                      
        X : array-like                                                              
            Training data.                                                          
                                                                                
        Returns                                                                     
        -------                                                                     
        pca_scores, fa_scores : tuple of arrays                                     
        """                                                                         
        pca = PCA(svd_solver='full')                                                
        fa = FactorAnalysis(max_iter=max_iter, tol=tol)                             
                                                                                
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
                                                                                
        return pca_scores, fa_scores


    def transform(self, data=None):                                            
        return {"pca": self.pca, "fa": self.fa}

import numpy as np
from sklearn.decomposition import PCA
from ..base import DataCleaningPrimitiveBase


class PCAFeatures(DataCleaningPrimitiveBase):

    def fit(self, intype, data):
        """ Do PCA and return the ranked features.                                  
                                                                                
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
                                                                                
        "importance_onallpcs" corresponds to the indices of the one most        
        important feature for each principal components.                        
                                                                                
        "explained_variance_ratio" Percentage of variance explained by each of  
        the selected components.                                                
        
        Params 
        ------- 
        intype : str
            Expect ``matrix``.
        data : array-like, [n_samples, n_features]
            Training data.
        """  
        if isinstance(intype, (list, tuple)):
            assert(intype[0]=="matrix")
        else:
            raise ValueError("Fit expected a 'matrix' an a intype.")

        pca = PCA()
        pca.fit_transform(data)

        self.components_ = pca.components_
        self.explained_variance_ratio_ = pca.explained_variance_ratio_

        M = np.absolute(pca.components_.T)
        # Rank features based on contribtuions to 1st PC
        self.importance_on1stpc = np.argsort(M[:,0], axis=0)[::-1]
        # Rank features based on contributions to PCs 
        self.importance_onallpcs = np.argmax(M, axis=0)

        return self

    def transform(self, data=None):
        return {
            "importance_on1stpc": self.importance_on1stpc,
            "importance_onallpcs": self.importance_onallpcs
        }

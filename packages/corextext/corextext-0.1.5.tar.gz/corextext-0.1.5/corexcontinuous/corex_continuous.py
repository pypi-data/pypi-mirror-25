from sklearn import preprocessing
#import primitive
import sys
import os
import linearcorex.linearcorex.linearcorex as corex_cont
#import LinearCorex.linearcorex as corex_cont
from collections import defaultdict
from scipy import sparse
import pandas as pd
import numpy as np

sys.path.append('../')
from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from typing import NamedTuple, Union, Optional, Sequence


Input = pd.DataFrame
Output = np.ndarray
Params = NamedTuple('Params', [
    ('latent_factors', np.ndarray),  # Coordinates of cluster centers.
])


class CorexContinuous(UnsupervisedLearnerPrimitiveBase):  #(Primitive):
    def __init__(self, n_hidden : int = None, latent_pct : float = None, max_iter : int = 10000, 
            tol : float = 1e-5, anneal : bool = True, discourage_overlap : bool = True, gaussianize : str = 'standard',  
            gpu : bool = False, verbose : bool = False, seed : int = None, **kwargs) -> None:
        
        super().__init__()

        self.kwargs = kwargs
        self.max_iter = max_iter
        self.tol = tol
        self.anneal = anneal
        self.discourage_overlap = discourage_overlap
        self.gaussianize = gaussianize
        self.gpu = gpu
        self.verbose = verbose
        self.seed = seed

        self.is_feature_selection = False
        self.hyperparameters = {'n_hidden': 2} # NOT TRUE, default = latent pct
        
        if n_hidden:
            self.n_hidden = n_hidden
            self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = max_iter, tol = tol, 
                anneal = anneal, discourage_overlap = discourage_overlap, gaussianize = gaussianize, 
                gpu = gpu, verbose = verbose, seed = seed, **kwargs)
        else:
            if latent_pct is None:
                self.latent_pct = .10 # DEFAULT = 10% OF ORIGINAL FACTORS
            else:
                self.latent_pct = latent_pct
            self.model = None


        # if latent_pct is not None and n_hidden is None:
        # 	self.n_hidden = int(len(self.columns)*latent_pct)
        # else:
        # 	self.n_hidden = 2 if n_hidden is None else n_hidden #DEFAULT = 2 

    def fit(self) -> None:
        if self.fitted:
            return
        if not self.training_inputs:
            raise ValueError("Missing training data.")

        self.fit_transform(self.training_inputs)
        self.fitted = True
        return self

    def produce(self, X : Sequence[Input], y : Sequence[Input] = None) -> Sequence[Output]: 

        self.columns = list(X)
        X_ = X[self.columns].values 
    	
       

        if not self.fitted:
            if self.model is None and self.latent_pct:
                self.n_hidden = int(self.latent_pct*len(self.columns))
                self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = self.max_iter, tol = self.tol, 
                    anneal = self.anneal, discourage_overlap = self.discourage_overlap, gaussianize = self.gaussianize, 
                    gpu = self.gpu, verbose = self.verbose, seed = self.seed, **self.kwargs)

            self.factors = self.model.fit_transform(X_)
        else:
            self.factors = self.model.transform(X_)

        return self.factors

    def fit_transform(self, X : Sequence[Input], y : Sequence[Input] = None) -> Sequence[Output]:
        
        self.columns = list(X)
     	X_ = X[self.columns].values

        if not self.n_hidden:
            self.n_hidden = int(self.latent_pct*len(self.columns))

        if self.model is None and self.latent_pct:
        	self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = self.max_iter, tol = self.tol, 
                anneal = self.anneal, discourage_overlap = self.discourage_overlap, gaussianize = self.gaussianize, 
                gpu = self.gpu, verbose = self.verbose, seed = self.seed, **self.kwargs)

    	self.factors = self.model.fit_transform(X_)
        self.fitted = True
        return self.factors

    def set_training_data(self, X : Sequence[Input]) -> None:
        self.training_inputs = X
        self.fitted = False

    def get_params(self) -> Params:
        return Params(latent_factors = self.factors)

    def annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'CorexContinuous'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'UnsupervisedLearning'
        self._annotation.ml_algorithm = ['Dimension Reduction']
        self._annotation.tags = ['feature_extraction'] #'continuous'
        return self._annotation

    def get_feature_names(self):
    	return ['CorexContinuous_'+ str(i) for i in range(self.n_hidden)]


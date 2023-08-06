import os
from typing import NamedTuple, Union, List, Sequence, Any
from typing import TypeVar

import numpy as np
from d3m_types.sequence import ndarray

import STMB_FeatureSelection_primitive
import scipy.io
from supervised_learning import SupervisedLearnerPrimitiveBase

# These are just regular Python variables so that we can easily change all types
# at once in the future, if needed. Otherwise, one could simply inline all these.
Inputs = ndarray
Outputs = ndarray
Params = TypeVar('Params')

class STMBFeatSelector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    """
    This class implements a feature selection method:

    It automatically select features that best fit the labels

    Input:

    A: Collection of vectors in high dimensional space.
    Concretely, inputs are doubly-indexable numbers that can be called as A[i,j].
    Rows i are samples and columns j are features.
    The entries can be integer, continuous values or categorical values,
    but should be expressed in a numerical form.

    B: The corresponding labels as a vector in a numerical form. This should be a
    row vector, and the length should be identical to the number of raw in A


    Output:

    W: Dimensionality reduced vectors, it is a numpy matrix with one row per vector.
    """

    def __init__(self):
        super().__init__()

        self.is_feature_selection = True
        self.hyperparameters = {}
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False

    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False

    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('datamat.mat',
                         mdict={'traindata': self.training_inputs, 'traintargets': self.training_outputs})
        my_stmb = STMB_FeatureSelection_primitive.initialize()

	    print('fit() method, call STMB Matlab code starts here ......')
        index = np.array(my_stmb.STMB_binsearch())
        print(index.shape)

        if index.shape == ():
            raise ValueError('Feature selection failed.')

        index = np.reshape(index, [index.shape[0], ])
        self.hyperparameters['index'] = (index - 1).astype(int)
        os.remove('datamat.mat')

        return True

    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if 'index' in self.hyperparameters.keys():
            return inputs[:, self.hyperparameters['index']]
        else:
            # print 'Please fit the model first using X = model.fit(training_data, training_labels)'
            raise ValueError('Model should be fitted first.')

    '''
    def fit_transform(self, A, B):

            scipy.io.savemat('datamat.mat', mdict={'traindata': A, 'traintargets': B})
        my_stmb = STMB_FeatureSelection_primitive.initialize()
        W = np.array(my_stmb.STMB_binsearch())
        os.remove('datamat.mat')

            return W

    '''
    fit.__annotations__ = {'A': 'NumpyArray(m x n)', 'B': 'NumpyArray(m x 1)', 'return': None}
    produce.__annotations__ = {'A': 'NumpyArray(m x n)', 'return': 'NumpyArray(m x k)'}

    def get_params(self):
        pass

    def set_params(self):
        pass

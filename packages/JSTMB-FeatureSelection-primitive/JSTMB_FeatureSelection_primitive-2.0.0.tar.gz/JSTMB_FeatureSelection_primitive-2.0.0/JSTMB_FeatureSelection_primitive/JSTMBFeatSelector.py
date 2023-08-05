import os
import JSTMB_FeatureSelection_primitive
import numpy as np
import scipy.io
from primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase


class JSTMBFeatSelector(SupervisedLearnerPrimitiveBase):
	"""
	This class implements a feature selection method:

	It automatically select features that best fit the labels

	Input:

	A: Collection of vectors in high dimensional space.
	Concretely, inputs are doubly-indexable numbers that can be called as A[i,j].
	Rows i are samples and columns j are features.
	The entries can be interger, continuous values or categorical values,
	but should be expressed in a numerical form.

	B: The corresponding labels as a vector in a numerical form. This should be a
	row vector, and the length should be identifcal to the number of raw in A


	Output:

	W: Dimensionality reduced vectors, it is a numpy matrix with one row per vector.
	"""

	def __init__(self):
		super(SupervisedLearnerPrimitiveBase, self).__init__()

		self.is_feature_selection = True
        	self.hyperparameters = {}
        	self.training_inputs = None
        	self.training_outputs = None
        	self.fitted = False

    	def set_training_data(self, inputs, outputs):
        	self.training_inputs = inputs
        	self.training_outputs = outputs
        	self.fitted = False

    	def fit(self):
        	if self.fitted:
            		return True

        	if self.training_inputs.any() == None or self.training_outputs.any() == None:
            		raise ValueError('Missing training data, or missing values exist.')

        	scipy.io.savemat('datamat.mat',
                         mdict={'traindata': self.training_inputs, 'traintargets': self.training_outputs})
        	my_jstmb = JSTMB_FeatureSelection_primitive.initialize()
        	index = np.array(my_jstmb.JSTMB_binsearch())
        	print index.shape

        	index = np.reshape(index, [index.shape[0], ])
        	self.hyperparameters['index'] = (index - 1).astype(int)
        	os.remove('datamat.mat')

        	return True

    	def produce(self, inputs):  # inputs: m x n numpy array
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









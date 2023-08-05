import scipy.io 
import os
import numpy as np 
import JSTMB_FeatureSelection_primitive


class JSTMBFeatSelector:
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

	is_feature_selection = True
	hyperparameters = {}


	def __init__(self):
    		return None


	def fit_transform(self, A, B):

    		scipy.io.savemat('datamat.mat', mdict={'traindata': A, 'traintargets': B})
		my_jstmb = JSTMB_FeatureSelection_primitive.initialize()
		W = np.array(my_jstmb.JSTMB_binsearch())
		os.remove('datamat.mat')

    		return W


    	fit_transform.__annotations__ = {'A': 'NumpyArray(m x n)', 'B': 'NumpyArray(m x 1)', 'return': 'NumpyArray(m x k)'}



""" usage example """

if __name__ == "__main__":
	import JSTMB_FeatureSelection_primitive
	import numpy as np
	import scipy.io
	import os
	from JSTMB_FeatureSelection_primitive import JSTMBFeatSelector
	jstmb = JSTMBFeatSelector.JSTMBFeatSelector()
	W = jstmb.fit_transform(A, B)

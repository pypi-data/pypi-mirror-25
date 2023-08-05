import numpy as np

class LinearRegression(object):
	"""docstring for linear_regression"""
	def __init__(self, X, y):
		super(LinearRegression, self).__init__()
		self.X_train = np.array(X)
		self.y_train = np.array(y)

	def fit(self, num_iters, alpha):
		self.coeff__ = np.zeros(self.X_train.shape[1]) #Number of Columns
		m = self.y_train.size #Number of examples
		factor = (alpha/m)

		self.costH = np.zeros(num_iters)

		for iter in range(1,num_iters):
			cost = self.computeCostMulti(self.X_train, self.y_train, self.coeff__) #Get Error
			htheta = self.X_train.dot(self.coeff__)

			correctionX = np.dot(self.X_train.T, (htheta - self.y_train))
			correctionFactor = correctionX * factor

			self.coeff__ = self.coeff__ - correctionFactor

			self.costH[iter] = cost


	def predict(self, X):
		return np.dot(X, self.coeff__)

	def computeCostMulti(self, X, y, theta):
		X = np.array(X)
		y = np.array(y)
		theta = np.array(theta)

		m = y.size #Number of examples

		J = X.dot(theta)
		J = ((sum((J-y)**2)))/(0.5 * m)
		return J
		
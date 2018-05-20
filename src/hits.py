import numpy as np
import scipy.sparse as sparse
import time
import pickle
from dataset_fetcher import ListToMatrixConverter
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import time

debug = False

class HITS():
	"""An instance of HITS is used to model the idea of hubs and authorities
	and execute the corresponding algorithm
	"""

	def __init__(self, link_matrix, users, index_id_map, is_sparse=False):
		"""
		Initializes an instance of HITS

		Args:
			link_matrix: The link matrix
			users: Details of all users
			index_id_map: Dictionary representing a map from link matrix index
			to user id
			is_sparse: True if the links matrix is a sparse matrix
		"""
		self.__is_sparse = is_sparse
		self.__link_matrix = link_matrix
		self.__link_matrix_tr = link_matrix.transpose()
		self.__n = self.__link_matrix.shape[0]
		self.__hubs = np.ones(self.__n)
		self.__auths = np.ones(self.__n)
		self.__size = 30

	def calc_scores(self, epsilon=1e-4):
		"""Calculates hubbiness and authority
		"""
		epsilon_matrix = epsilon * np.ones(self.__n)
		if self.__is_sparse:
			while True:
				hubs_old = self.__hubs
				auths_old = self.__auths

				self.__auths = self.__link_matrix_tr * hubs_old
				max_score = self.__auths.max(axis=0)
				if max_score != 0:
					self.__auths = self.__auths / max_score

				self.__hubs = self.__link_matrix * self.__auths
				max_score = self.__hubs.max(axis=0)
				if max_score != 0:
					self.__hubs = self.__hubs / max_score

				if (((abs(self.__hubs - hubs_old)) < epsilon_matrix).all()) and (((abs(self.__auths - auths_old)) < epsilon_matrix).all()):
					break

		else:
			while True:
				hubs_old = self.__hubs
				auths_old = self.__auths

				self.__auths = np.dot(self.__link_matrix_tr, hubs_old)
				max_score = self.__auths.max(axis=0)
				if max_score != 0:
					self.__auths = self.__auths / max_score

				self.__hubs = np.dot(self.__link_matrix, self.__auths)
				max_score = self.__hubs.max(axis=0)
				if max_score != 0:
					self.__hubs = self.__hubs / max_score

				if (((abs(self.__hubs - hubs_old)) < epsilon_matrix).all()) and (((abs(self.__auths - auths_old)) < epsilon_matrix).all()):
					break

	def get_scores(self):
		return (self.__hubs, self.__auths)

class DatasetReader():
	"""An instance of DatasetReader is used to read different files from the
	dataset
	"""

	def __init__(self):
		"""Initializes an instance of DatasetReader
		"""
		pass

	def read_users(self, users_path):
		"""Returns the dictionary (stored in a file) containing details of
		all users

		Args:
			users_path: Path to the file where info of all users is stored
		"""
		with open(users_path, mode='rb') as f:
			users = pickle.load(f)
		return users

	def read_map(self, map_path):
		"""Returns the dictionary (stored in a file) that represents a map
		from the link matrix index to user id

		Args:
			map_path: Path to the file where the map is stored
		"""
		with open(map_path, mode='rb') as f:
			index_id_map = pickle.load(f)
		return index_id_map

	def read_link_matrix(self, link_matrix_path, is_sparse=False):
		"""Returns the array (stored in a file) that represents the link matrix

		Args:
			link_matrix_path: Path to the file where the link matrix is stored
			is_sparse: True if the link matrix is stored as a sparse matrix
		"""
		with open(link_matrix_path, mode='rb') as f:
			if is_sparse:
				link_matrix = sparse.load_npz(link_matrix_path)
			else:
				link_matrix = np.load(f)
		return link_matrix


def main():
	sparse = False
	epsilon = 1e-10
	show_iters = True

	users_path = '../data/users'
	map_path = '../data/map'
	sparse_link_matrix_path = '../data/sparse_link_matrix'
	dense_link_matrix_path = '../data/dense_link_matrix'
	if sparse:
		link_matrix_path = sparse_link_matrix_path
	else:
		link_matrix_path = dense_link_matrix_path

	# Load the stored data into objects
	r = DatasetReader()
	users = r.read_users(users_path)
	index_id_map = r.read_map(map_path)
	link_matrix = r.read_link_matrix(link_matrix_path, is_sparse=sparse)

	# Run the algorithm
	h = HITS(link_matrix, users, index_id_map, is_sparse=sparse)
	h.calc_scores(epsilon=epsilon)
	print(h.get_scores())

if __name__ == '__main__':
	main()
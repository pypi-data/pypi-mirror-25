""" Module for the base abstract class of DynaMIT
MotifSearcher component.
"""
from __future__ import print_function
from __future__ import division

from builtins import str
from future.utils import with_metaclass

from abc import ABCMeta, abstractmethod

class MotifSearcher(with_metaclass(ABCMeta)):
	"""Class representing a MotifSearch component,
	providing a logic to execute a motif search tool on a set
	of input sequences; components implementing this interface
	will be run during DynaMIT phase 1, i.e. motif search.
	"""

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		self.searcherName = ""
		self.searchResults = []
		self.path = ""
		self.params = ""

	@abstractmethod
	def setConfiguration(self, path, params):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			path: path of the tool executable file.
			params: parameters to be given to the tool along with the sequences filename.

		Returns:
			Returns 0 if everything went fine, 1 and an error message otherwise.
		"""
		return 1

	@abstractmethod
	def runSearch(self, sequencesFilename):
		"""Performs motif search.

		Args:
			sequencesFilename: input sequences filename for this run.

		Returns:
			Returns a list of strings representing identified motif matches
			if everything went fine (details on results filenames, etc.,
			are printed to the console); returns 1 and an error message otherwise.
		"""
		return 1

	def getResults(self):
		"""Returns the integration results dictionary
		produced by a call to runSearch().
		"""
		return self.searchResults

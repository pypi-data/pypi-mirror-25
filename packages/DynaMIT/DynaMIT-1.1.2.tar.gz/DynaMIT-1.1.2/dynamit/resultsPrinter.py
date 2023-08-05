""" Module for the base abstract class of DynaMIT
ResultsPrinter component.
"""
from __future__ import print_function
from __future__ import division

from builtins import str
from future.utils import with_metaclass

from abc import ABCMeta, abstractmethod

class ResultsPrinter(with_metaclass(ABCMeta)):
	"""Class representing a ResultsPrinter component,
	providing a logic to print the results of motif
	integration, obtained through DynaMIT phase 2.
	"""

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		self.resultsPrinterName = ""

	@abstractmethod
	def setConfiguration(self, configString):
		"""Loads the printer parameters specified in the configuration file.

		Args:
			configString: the configuration string derived from the run configuration
										filename (provided by the Runner component).

		Returns:
			Returns 0 if everything went fine, 1 and an error message otherwise.
		"""
		return 1

	@abstractmethod
	def printResults(self, sequences, searchResults,
									 integrationStrategyName, integrationResults):
		"""Performs the results printing.

		Args:
			sequences: collection of input sequences for this run.
			searchResults: table containing matches for all motifs on all sequences.
										This table is produced by DynaMIT motif search phase.
			integrationStrategyName: name of the strategy used to perform
															 the integration step.
			integrationResults: dictionary of results produced by the
													integration step.

		Returns:
			Returns 0 if everything went fine (details on results filenames, etc.,
			are printed to the console); returns 1 and an error message otherwise.
		"""
		return 1

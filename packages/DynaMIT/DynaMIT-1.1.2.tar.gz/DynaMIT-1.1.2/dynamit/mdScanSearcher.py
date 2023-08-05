"""Module for MDscanSearcher classes."""

from __future__ import print_function
from __future__ import division

from builtins import str

import os, re
import subprocess
from subprocess import CalledProcessError

import dynamit.motifSearcher
import dynamit.utils

class MDscanSearcher(dynamit.motifSearcher.MotifSearcher):
	"""Class implementing a MDscan motif search component,
	running the MDscan tool on the provided input sequences,
	eventually providing its processed motifs and instances.
	"""
	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__()
		self.searcherName = "MDscan"
		self.path = ""
		self.params = ""

	def setConfiguration(self, path, params):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			path: path of the MDscan executable file.
			params: parameters to be passed to MDscan
							along with the sequences filename.

		Returns:
			Returns 0 if everything went fine, 1 and an error message otherwise.
		"""
		if path != "":
			self.path = path
		if params != "":
			self.params = params
		return 0

	def runSearch(self, sequencesFilename):
		"""Performs motif search by executing the MDscan
		motif search tool and processing its results
		to provide motifs and related instances.

		Args:
			sequencesFilename: input sequences filename for this run.

		Returns:
			Returns a list of strings representing identified motif matches
			if everything went fine (details on results filenames, etc.,
			are printed to the console); returns 1 and an error message otherwise.
		"""

		# prepare sequences dictionary to be later passed to processMDscanResults.
		sequences = dict([(seqRecord.description, str(seqRecord.seq)) \
				for seqRecord in dynamit.utils.getSequencesRecords(sequencesFilename)])

		# compose the complete command-line for launching MDscan.
		completePath = os.path.join(self.path, "MDscan") + " -i \"" + \
									 sequencesFilename + "\" " + self.params

		try:
			# launch MDscan and wait for its execution to
			# complete (its output is redirected to the callOutput variable).
			callOutput = subprocess.check_output(completePath, shell=True,
																					 stderr=subprocess.STDOUT)
			# extract results from MDscan output files.
			print("  [MDscanSearcher] Search completed.")
			self.searchResults = self._processMDscanResults(sequences,
																											callOutput)
		except CalledProcessError as e:
			# inform about the error that happened,
			print("[ERROR] MDscan execution terminated with an error:" + e.output)
			# abort searcher execution.
			return 1

		# inform of successful execution and return the results.
		print("  [MDscanSearcher] Execution completed.")
		return self.searchResults

	def _processMDscanResults(self, sequences, results):
		""" Process results contained in MDscan output to
		produce a table for subsequent DynaMIT phases.

		Args:
			sequences: a dictionary of sequences (id is key, sequence is value).
			results: the MDscan results text.
		Returns:
			Returns a list of strings, one per motif match, containing
			motif sequence, sequence id, match position, etc.
		"""
		processedResults = []

		try:
			# get results lines from MDscan output.
			lines = results.split('\n')

			lineIndex = 0
			inMotifSites = False
			currentMotifConsensus = ""
			currentMotifScore = ""
			while lineIndex < len(lines):
				# start of new motif: must match "	Motif N sites",
				# i.e. motif sites header line.
				if re.match(r"Motif\s[0-9]+:\s", lines[lineIndex]):
					# get the new motif consensus.
					info = re.split(r';', lines[lineIndex].rstrip('\n'))
					currentMotifConsensus = info[3].lstrip(' Con ')
					currentMotifScore = info[1].lstrip(' Score ')
					# move to the first motif site line
					lineIndex += len(currentMotifConsensus) + 3
					inMotifSites = True
				# matches the end of motif sites lines
				elif lines[lineIndex].startswith("****************************"):
					inMotifSites = False
				# this is a motif site line
				elif inMotifSites:
					if lines[lineIndex].startswith(">"):
						info = lines[lineIndex].lstrip(">").rstrip('\n').split('\t')
						# get forward match positions according to f/r strand.
						start = 0
						if info[3].startswith("f"):
							start = int(info[3].lstrip('f '))
						else:
							start = int(info[1].lstrip('Len ')) - int(info[3].lstrip('r ')) -\
											len(currentMotifConsensus) + 1
						end = start + len(currentMotifConsensus)
						# append current motif match to results in DynaMIT format
						fullSeqID = dynamit.utils.getFullSequenceID(sequences, info[0], end)
						fullSeqID = info[0] if fullSeqID == -1 else fullSeqID
						processedResults.append(currentMotifConsensus + "\tsequence\t" + \
																	self.searcherName + "\t" + fullSeqID + \
																	"\t" + str(start) + "\t" + str(end) + \
																	"\t" + currentMotifScore)
				lineIndex += 1

			return processedResults
		except (IOError, IndexError, ValueError, RuntimeError) as e:
			print("  [MDscanSearcher] Unexpected error: %s" % str(e))
			return 1

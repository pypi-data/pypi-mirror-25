"""Module for HOMERSearcher classes."""

from __future__ import print_function
from __future__ import division

from builtins import str

import os
import subprocess
from subprocess import CalledProcessError

import dynamit.motifSearcher
import dynamit.utils

class HOMERSearcher(dynamit.motifSearcher.MotifSearcher):
	"""Class implementing a HOMER motif search component,
	running the HOMER tool on the provided input
	sequences (plus background sequences specified in
	the configuration), eventually providing its processed
	motifs and instances.
	"""
	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__()
		self.searcherName = "HOMER"
		self.path = ""
		self.params = ""
		self.backgroundFilename = ""

	def setConfiguration(self, path, params):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			path: path of the HOMER executable file.
			params: parameters to be passed to HOMER
							along with the sequences filename.

		Returns:
			Returns 0 if everything went fine, 1 and an error message otherwise.
		"""
		if path != "":
			self.path = path
		if params != "":
			info = params.split(',')
			# store background sequences filename.
			self.backgroundFilename = info[0]
			# store additional parameters, if any.
			if len(info) > 1:
				self.params = info[1]

		if self.backgroundFilename == "":
			print("[ERROR] Background sequences filename " \
						"specification missing.")
			return 1

		return 0

	def runSearch(self, sequencesFilename):
		"""Performs motif search by executing the HOMER
		motif search tool and processing its results
		to provide motifs and related instances.

		Args:
			sequencesFilename: input sequences filename for this run.

		Returns:
			Returns a list of strings representing identified motif matches
			if everything went fine (details on results filenames, etc.,
			are printed to the console); returns 1 and an error message otherwise.
		"""

		# prepare sequences dictionary to be later passed to processHOMERResults.
		sequences = dict([(seqRecord.description, str(seqRecord.seq)) \
				for seqRecord in dynamit.utils.getSequencesRecords(sequencesFilename)])

		try:
			# launch HOMER to perform motif identification ("denovo" mode).
			completePath = os.path.join(self.path, "homer2 denovo") + \
										 " -i \"" + sequencesFilename + \
										 "\" -b \"" + self.backgroundFilename + "\" " + \
										 self.params + "  > HOMER.motifs"
			subprocess.check_output(completePath, shell=True, stderr=subprocess.STDOUT)

			if os.path.isfile("HOMER.motifs"):
				print("  [HOMERSearcher] Motifs identified.")

				# then launch HOMER to perform motif instances finding ("find" mode).
				completePath = os.path.join(self.path, "homer2 find") + \
										 " -i \"" + sequencesFilename + \
										 "\" -m HOMER.motifs -offset 1 > HOMER.instances"
				subprocess.check_output(completePath, shell=True, stderr=subprocess.STDOUT)

				if os.path.isfile("HOMER.instances"):
					print("  [HOMERSearcher] Motifs instances found.")
					# extract results from HOMER output files.
					self.searchResults = self._processHOMERResults(sequences,
																												"HOMER.instances")
					# inform of successful execution and return the results.
					print("  [HOMERSearcher] Execution completed.")
					return self.searchResults
				else:
					print("[ERROR] Could not find HOMER results (motif instances) file.")
					return 1
			else:
				print("[ERROR] Could not find HOMER results (motifs) file.")
				return 1
		except CalledProcessError as e:
			# inform about the error that happened,
			print("[ERROR] HOMER execution terminated with an error:" + e.output)
			# abort searcher execution.
			return 1

	def _processHOMERResults(self, sequences, resultsFilename):
		""" Process results contained in HOMER output files to
		produce a table for subsequent DynaMIT phases.

		Args:
			sequences: a dictionary of sequences (id is key, sequence is value).
			resultsFilename: the HOMER results filename.
		Returns:
			Returns a list of strings, one per motif match, containing
			motif sequence, sequence id, match position, etc.
		"""
		processedResults = []

		try:
			# get results lines from HOMER output files.
			with open(resultsFilename) as f:
				lines = f.readlines()

			lineIndex = 0
			while lineIndex < len(lines):
				if lines[lineIndex] != '':
					info = lines[lineIndex].rstrip('\n').split('\t')
					# get forward match positions according to f/r strand.
					start = info[1]
					if info[4] == "+":
						end = str(int(start) + len(info[2]))
					else:
						end = str(int(start) + 1)
						start = str(int(end) - len(info[2]))
					# append current motif match to results in DynaMIT format
					fullSeqID = dynamit.utils.getFullSequenceID(sequences, info[0],
																		int(info[1]) + len(info[2]))
					fullSeqID = info[0] if fullSeqID == -1 else fullSeqID
					processedResults.append(info[3].split('-')[1] + "\tsequence\t" + \
																	self.searcherName + "\t" + \
																	fullSeqID + "\t" + start + "\t" + \
																	end + "\t" + info[5] + "\t" + info[4])
				lineIndex += 1

			return processedResults
		except (IOError, IndexError, ValueError, RuntimeError) as e:
			print("  [HOMERSearcher] Unexpected error: %s" % str(e))
			return 1

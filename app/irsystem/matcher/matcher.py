import numpy as np

# Number of best match characters returned (besides the best match)
NUM_MATCH = 5

class Matcher(object):
	def __init__(self):
		pass

	def __calc_bigfive(self, results):
		pass

	# Returns the information for best matching characters
	# results is an array of 10 numbers ranging 1-7 for the personality test
	def match(self, results):
		return '%s is the input' % results
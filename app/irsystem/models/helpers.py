# Methods to compose HTTP response JSON 
from flask import jsonify
import base64
import json
import numpy as np
import os
import csv


# Number of best match characters returned (besides the best match)
NUM_MATCH = 5

DATA_PATH = 'data/personality/char_big_five/'


sanitize = lambda s: s[:s.find(' ')] if ' ' in s else s
capt = lambda s: ' '.join(map(lambda a: a.capitalize(), s.split('_')))

# name: path for the csv file containing big 5 information
# returns: parsed movie / TV name, character names, big-five matrix

# Bigfive order: 
# aggreableness, extraversion, conscientious, neuroticism, openess
def read_csv(name):
	series_name = capt(name[name.rfind('/')+1:-4])
	char_names, char_vecs = [], []
	lst = []
	with open(name) as f:
		reader = csv.reader(f, delimiter = '\t')
		for row in reader:
			lst.append(row)
	for item in lst[1:]:
		cname = capt(sanitize(item[0]))
		cvec = np.array(list(map(float, item[-5:])))
		char_names.append(cname)
		char_vecs.append(cvec)
	return series_name, char_names, np.array(char_vecs)



class Matcher(object):
	def __init__(self):
		cur_id = 0
		self.chars = {} # character id to char name
		self.series = {} # char id to movie / TV name
		self.bigfive = None
		files = os.listdir(DATA_PATH)
		for file in files:
			if file[0] == '.': continue
			sname, names, vecs = read_csv(DATA_PATH + file)
			for nm in names:
				self.chars[cur_id] = nm
				self.series[cur_id] = sname
				cur_id += 1
			if self.bigfive is None:
				self.bigfive = vecs
			else:
				self.bigfive = np.concatenate((self.bigfive, vecs))
		# print(self.bigfive)


	def __calc_bigfive(self, results):
		assert len(results) == 10, 'must provide 10 answers for bigfive quiz'
		ans = np.zeros(5)
		ans[1] = results[0] + 8 - results[5]
		ans[0] = results[6] + 8 - results[1]
		ans[2] = results[2] + 8 - results[7]
		ans[3] = results[8] + 8 - results[3]
		ans[4] = results[4] + 8 - results[9]
		return (ans - 8.) / 6

	# Returns the information for best matching characters
	# results is an array of 10 numbers ranging 1-7 for the personality test
	def match(self, results):
		vec = self.__calc_bigfive(results)
		indices = np.sum((vec * self.bigfive) ** 2, axis = 1).argsort()
		nearest = indices[0]
		print(vec, self.chars[nearest], self.series[nearest], self.bigfive[nearest])
		return 'You are most similar to %s in %s' % \
			(self.chars[nearest], self.series[nearest])


def http_json(result, bool):
	result.update({ "success": bool })
	return jsonify(result)

def http_resource(result, name, bool=True):
	resp = { "data": { name : result }}
	return http_json(resp, bool)

def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)

class NumpyEncoder(json.JSONEncoder):

	def default(self, obj):
		"""If input object is an ndarray it will be converted into a dict 
		holding dtype, shape and the data, base64 encoded.
		"""
		if isinstance(obj, np.ndarray):
			if obj.flags['C_CONTIGUOUS']:
				obj_data = obj.data
			else:
				cont_obj = np.ascontiguousarray(obj)
				assert(cont_obj.flags['C_CONTIGUOUS'])
				obj_data = cont_obj.data
			data_b64 = base64.b64encode(obj_data)
			return dict(__ndarray__=data_b64,
						dtype=str(obj.dtype),
						shape=obj.shape)
		# Let the base class default method raise the TypeError
		return json.JSONEncoder(self, obj)
		
def json_numpy_obj_hook(dct):
	"""Decodes a previously encoded numpy ndarray with proper shape and dtype.
	:param dct: (dict) json encoded ndarray
	:return: (ndarray) if input was an encoded ndarray
	"""
	if isinstance(dct, dict) and '__ndarray__' in dct:
		data = base64.b64decode(dct['__ndarray__'])
		return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
	return dct





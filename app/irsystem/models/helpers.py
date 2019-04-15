# Methods to compose HTTP response JSON 
from flask import jsonify
import base64
import json
import numpy as np
import os
import csv
from collections import defaultdict


# Number of best match characters returned (besides the best match)
NUM_MATCH = 1

DATA_PATH = 'data/personality/char_big_five/'
QUOTE_PATH = 'data/personality/all_characters.json'


sanitize = lambda s: s[:s.find(' ')] if ' ' in s else s
capt = lambda s: ' '.join(s.split('_'))


# name: path for the csv file containing big 5 information
# returns: parsed movie / TV name, character names, big-five matrix

# Bigfive order: 
# aggreableness, extraversion, conscientious, neuroticism, openess
def read_csv(name):
	series_name = capt(name[name.rfind('/')+1:-4])
	series_name = ' '.join(list(map(lambda s: s.capitalize(), series_name.split(' '))))
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
		self.ids = {} # character name to id
		self.series = {} # char id to movie / TV name
		self.bigfive = None
		self.quotes = defaultdict(str)
		files = os.listdir(DATA_PATH)
		for file in files:
			if file[0] == '.': continue
			sname, names, vecs = read_csv(DATA_PATH + file)
			for nm in names:
				self.chars[cur_id] = nm
				self.ids[nm] = cur_id
				self.series[cur_id] = sname
				cur_id += 1
			if self.bigfive is None:
				self.bigfive = vecs
			else:
				self.bigfive = np.concatenate((self.bigfive, vecs))
		with open(QUOTE_PATH) as f:
			j = json.load(f)
		for char in j:
			nm = char.replace('_', ' ')
			if nm in self.ids:
				cid = self.ids[nm]
				quote = ' '.join(j[char].get('quote', []))
				if quote and quote[0] == '"': quote = quote[1:]
				if quote and quote[-1] == '"': quote = quote[:-1]
				self.quotes[cid] = quote


	def __calc_bigfive(self, results):
		assert len(results) == 10, 'must provide 10 answers for bigfive quiz'
		ans = np.zeros(5)
		ans[1] = results[0] - results[5]
		ans[0] = results[6] - results[1]
		ans[2] = results[2] - results[7]
		ans[3] = results[3] - results[8]
		ans[4] = results[4] - results[9]
		return ans / 6


	'''
	Returns the information for best matching characters
	results is an array of 10 numbers ranging 1-7 for the personality test
	Returns (for now): 
			Char name list
			Movie/TV name list
			Quote list
			Char bigfive vector list
			User bigfive vector
	Each list has a length of NUM_MATCH, ranking from most to least similar
	'''
	def match(self, results):
		vec = self.__calc_bigfive(results)
		indices = np.linalg.norm(vec - self.bigfive, axis = 1).argsort()
		nearest = indices[:NUM_MATCH]
		cnames, mnames, quotes = [], [], []
		for i in nearest:
			cnames.append(self.chars[i])
			mnames.append(self.series[i])
			quotes.append(self.quotes[i])
		return cnames, mnames, quotes, self.bigfive[nearest], vec


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





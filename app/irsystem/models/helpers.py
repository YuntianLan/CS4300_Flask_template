# Methods to compose HTTP response JSON
from flask import jsonify
import base64
import json
import numpy as np
import os
import csv
import math
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer


# Number of best match characters returned (besides the best match)
NUM_MATCH = 5

# DATA_PATH = 'data/personality/char_big_five/'
DATA_PATH = 'data/personality/all_characters.json'
CU_MOVIE_DATA_PATH = 'data/personality/cornell_movie_characters_bigfive.json'
ALL_DATA = [DATA_PATH, CU_MOVIE_DATA_PATH]
REVIEWS_CU_PATH = "data/Movie Review/characters_review_cornell.json"
REVIEWS_OTHER_PATH = "data/Movie Review/characters_review_other.json"

DEFAULT_URL = 'https://www.google.com'
DEFAULT_DESCRIPTION = 'No description available'
DEFAULT_QUOTE, DEFAULT_SAID_BY = ('Nothing', 'No One')
FANDOM_NAMES = ["Game Of Thrones", "Harry Potter", "Marvel Cinematic Universe", "Star Wars",""]

ADJS_PATH = 'data/personality/big5.csv'

CHAR_LINES = [
	'data/all_character_lines.json',
	'data/char_quotes.json',
]

sanitize = lambda s: s[:s.find(' ')] if ' ' in s else s
capt = lambda s: ' '.join(list(map(lambda nm: nm.capitalize(), s.split(' '))))

weights = {
	'review': 0.5,
	'char': 0.1,
	'adjs': 0.1,
	'catchphrase': 0.1
}

def make_script(lst):
	ignore = ['.', '!', '?']
	script = ' '.join(lst)
	script = script.replace('...', ' ')
	for sign in ignore:
		script = script.replace(sign, '')
	return script.lower()

# name: path for the csv file containing big 5 information
# returns: parsed movie / TV name, character names, big-five matrix

# Bigfive order:
# aggreableness, extraversion, conscientious, neuroticism, openess


class Matcher(object):
	def load_json(self, ja):
		sorted_ja = sorted(ja.items(), key=lambda kv: kv[1]["series"])
		vecs = []
		review_counts = []
		for char in sorted_ja:
			d = char[1]
			name = d['name']
			vec = d['big_five']

			if not vec: continue

			movie = d.get('movie', '').title()
			series = d.get('series', '').title()
			if self.cur_fandom_ind<len(FANDOM_NAMES) and series==FANDOM_NAMES[self.cur_fandom_ind]:
				self.fandom_indices.append(self.cur_id)
				self.cur_fandom_ind+=1

			desc = d.get('description', DEFAULT_DESCRIPTION)
			url = d.get('url', DEFAULT_URL)
			quote, said_by = d.get('quote', (DEFAULT_QUOTE, DEFAULT_SAID_BY))
			if len(quote)==0: continue

			self.chars[self.cur_id] = name
			self.ids[name] = self.cur_id
			self.series[self.cur_id] = series
			self.movies[self.cur_id] = movie
			self.urls[self.cur_id] = url
			self.quotes[self.cur_id] = (quote, said_by)

			vecs.append(np.array(vec))
			if char[0] in self.reviews:
				review_count = self.reviews[char[0]]["review_count"]
			else:
				review_count = 0
			review_counts.append(self.scale_review_count(review_count))
			self.cur_id += 1

		if self.bigfive is None:
			self.bigfive = np.array(vecs)
			self.review_count = np.array(review_counts)
		else:
			self.bigfive = np.concatenate((self.bigfive, np.array(vecs)))
			self.review_count = np.concatenate((self.review_count, np.array(review_counts)))

		

	def __init__(self):
		self.cur_id = 0
		self.chars = {} # character id to char name
		self.ids = {} # character name to id
		self.movies = defaultdict(str) # char id to movie / TV name
		self.series = defaultdict(str) # char id to series name
		self.urls = defaultdict(lambda: DEFAULT_URL) # char id to char url
		self.bigfive = None
		# char id to (quote, said_by)
		self.quotes = defaultdict(lambda: (DEFAULT_QUOTE, DEFAULT_SAID_BY))
		self.fandom_indices=[]
		self.cur_fandom_ind = 0
		self.review_count = None

		self.adjs = {}
		with open(ADJS_PATH) as f:
			reader = csv.reader(f, delimiter = ',')
			for row in reader:
				adj = row[0].lower()
				vec = np.zeros(5, dtype = np.float32)
				for i, num in enumerate(row[1:]):
					vec[i] = float(num.replace('*', ''))
				self.adjs[adj] = vec

		self.weights = weights

		with open(REVIEWS_CU_PATH) as f:
			reviews_cu = json.loads(json.load(f))
		with open(REVIEWS_OTHER_PATH) as f:
			reviews_others = json.loads(json.load(f))
		self.reviews = {**reviews_cu, **reviews_others}

		for path in ALL_DATA:
			with open(path) as f:
				self.load_json(json.load(f))

		# Make tfidf vectorizer for all character scripts
		scripts_dict = {}
		for char_line_file in CHAR_LINES:
			jl = json.load(open(char_line_file))
			for k in jl:
				scripts_dict[k.replace('_', ' ')] = make_script(jl[k])
		scripts = [''] * self.cur_id
		for i in range(self.cur_id):
			if self.chars[i] in scripts_dict:
				scripts[i] = scripts_dict[self.chars[i]]
		self.tfidf = TfidfVectorizer(min_df = 5,
							max_df = 0.8, 
							max_features = 3000,
							stop_words = 'english', 
							norm = 'l2'
							)
		self.doc_vocab_mat = self.tfidf.fit_transform(scripts).toarray()
		self.doc_norms = np.linalg.norm(self.doc_vocab_mat, axis = 1)
		self.lookup = {i:v for i, v in enumerate(self.tfidf.get_feature_names())}


	def calc_bigfive(self, results):
		assert len(results) == 10, 'must provide 10 answers for bigfive quiz'
		ans = np.zeros(5)
		ans[1] = results[0] - results[5]
		ans[0] = results[6] - results[1]
		ans[2] = results[2] - results[7]
		ans[3] = results[3] - results[8]
		ans[4] = results[4] - results[9]
		return ans / 6


	def scale_review_count(self, c):
		return math.log(1+c)*0.01 #really small effect right now


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
	def match(self, results, fandoms, adj, catchphrase, char):
		# 1. Test bigfive
		vec = self.calc_bigfive(results)

		# 2. adj shift 
		adjs = adj.split(',')
		vec_shift = np.zeros(5)
		for adj in adjs:
			adj = adj.strip().lower()
			adj_vec = self.adjs.get(adj, np.zeros(5))
			vec_shift += adj_vec
		vec_shift = np.clip(vec_shift, -1, 1)
		vec += vec_shift * self.weights['adjs']

		# 3. Sim char shift
		sim_cid = self.chars.get(char.replace('_', ' '), -1)
		sim_char_bigfive = self.bigfive[sim_cid] if sim_cid != -1 else np.zeros(5)
		sim_char_weight = self.weights['char']
		for i in range(5):
			cur_sim = sim_char_bigfive[i]
			if abs(vec[i] - sim_char_bigfive[i]) < sim_char_weight:
				vec[i] = sim_char_bigfive[i]
			elif vec[i] < sim_char_bigfive[i]:
				vec[i] += abs(sim_char_bigfive[i])
			else:
				vec[i] -= abs(sim_char_bigfive[i])

		# 4. catchphrase cos sim
		cp_vec = self.tfidf.transform([make_script([catchphrase])]).toarray()
		if np.linalg.norm(cp_vec) == 0: cp_vec[0] += 1e-5
		dot_prod = (self.doc_vocab_mat * cp_vec).sum(axis = 1)
		cossim = dot_prod / (self.doc_norms * np.linalg.norm(cp_vec))
		angles = np.arccos(cossim) / np.pi # 0 - 3.14159 (pi), normalize

		# Filter fandom
		selected_inds = set()
		if len(fandoms)>0:
			for fandom in fandoms:
				if fandom+1>=len(self.fandom_indices):
					selected_inds.update(range(self.fandom_indices[fandom], len(self.bigfive)))
				else:
					selected_inds.update(range(self.fandom_indices[fandom],self.fandom_indices[fandom+1]))

		


		dists = np.linalg.norm(vec - self.bigfive, axis = 1) / (20**0.5) # normalize
		# 5. review
		dists -= self.weights['review'] * self.review_count
		dists -= self.weights['catchphrase'] * angles

		# Special case: groot, hodor
		if 'groot' in catchphrase:
			dists[self.ids['Groot']] = 0
		if 'hodor' in catchphrase or ('hold' in catchphrase and 'door' in catchphrase):
			dists[self.ids['Hodor']] = 0

		indices = dists.argsort()

		if len(fandoms)>0:
			selected_indices = [ind for ind in indices if ind in selected_inds]
		else:
			selected_indices = indices
		nearest = selected_indices[:NUM_MATCH]
		names, movies, series, quotes, urls = [], [], [], [], []
		vecs = self.bigfive[nearest]
		for (idx, i) in enumerate(nearest):
			# i = len(self.chars) - idx - 1
			names.append(self.chars[i])
			movies.append(self.movies[i])
			series.append(self.series[i])
			quotes.append(self.quotes[i])
			urls.append(self.urls[i])
		origins = []
		for i, movie in enumerate(movies):
			if movie and series[i]:
				s = '%s (%s)' % (movie, series[i])
			elif not movie:
				s = series[i]
			else:
				s = movie
			origins.append(s)
		return names, origins, quotes, urls, vecs, vec


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





import torch
import torch.nn as nn
import numpy as np
import json
import collections
from sklearn.feature_extraction.text import TfidfVectorizer


ignore = ['.', '!', '?']
MIN_OCCURENCE = 10
learning_rate = 5e-3
regularization = 0
num_epoch = 1000

max_df = 0.8
min_df = 5
max_features = 2000


def get_train_data():
	char_five = '../../data/personality/all_characters.json'
	char_lines1 = '../../data/all_character_lines.json'
	char_lines2 = '../../data/char_quotes.json'

	with open(char_five) as f: ja = json.load(f)
	with open(char_lines1) as f: jl = json.load(f)
	with open(char_lines2) as f: jl2 = json.load(f)
	for c in jl2:
		if c not in jl:
			jl[c] = jl2[c]

	unlabeled = {}; added = set()

	big_five, lines = [], []
	for c in ja:
		if c in jl:
			line = ' '.join(jl[c])
			line = line.replace('...', ' ')
			for sign in ignore:
				line = line.replace(sign, '')
			big_five.append(ja[c]['big_five'])
			lines.append(line.lower())
			added.add(c)
	for c in jl:
		if not c in added:
			line = ' '.join(jl[c])
			line = line.replace('...', ' ')
			for sign in ignore:
				line = line.replace(sign, '')
			unlabeled[c] = line

	return np.array(big_five, dtype = np.float32), lines, unlabeled

def train_model():
	big_five, lines, unlabeled = get_train_data()


	tfidf = TfidfVectorizer(min_df = min_df,
							max_df = max_df,
							max_features = max_features,
							stop_words = 'english',
							norm = 'l2'
							)
	doc_vocab_mat = tfidf.fit_transform(lines).toarray()
	lookup = {i:v for i, v in enumerate(tfidf.get_feature_names())}

	x_train = doc_vocab_mat.astype(np.float32)
	y_train = big_five
	n, d = x_train.shape



	# counts = collections.defaultdict(int)
	# for line in lines:
	# 	for w in line.split(' '):
	# 		counts[w] += 1
	# words = list(filter(lambda k: counts[k] > MIN_OCCURENCE, counts.keys()))

	# lookup = {}
	# for i, w in enumerate(words):
	# 	lookup[w] = i
	# n, d = len(lines), len(words)
	# x_train = np.zeros((n, d), dtype = np.float32)
	# y_train = big_five
	# for (i, line) in enumerate(lines):
	# 	for w in line.split(' '):
	# 		if w in lookup:
	# 			x_train[i, lookup[w]] += 1
	# # import pdb; pdb.set_trace()
	# invalid = np.sum(x_train, axis = 1) == 0
	# x_train /= np.sum(x_train, axis = 1).reshape(n, 1)

	# x_train[invalid] = 0

	# import pdb; pdb.set_trace()

	model = nn.Linear(d, 5)
	criterion = nn.MSELoss()
	optimizer = torch.optim.SGD(model.parameters(),
		lr = learning_rate, weight_decay = regularization)

	for epoch in range(num_epoch):
		indices = np.arange(n)
		np.random.shuffle(indices)

		x_in = torch.from_numpy(x_train[indices])
		y_in = torch.from_numpy(y_train[indices])

		outputs = model(x_in)
		loss = criterion(outputs, y_in)

		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epoch, loss.item()))

	torch.save(model.state_dict(), 'model.ckpt')
	with open('lookup.json', 'w+') as f:
		json.dump(lookup, f)
	return model, lookup, unlabeled, x_train, y_train, tfidf

def predict():
	model, lookup, unlabeled, x_train, y_train, tfidf = train_model()
	chars, lines = [], []
	for c in unlabeled:
		chars.append(c)
		lines.append(unlabeled[c])
	x = tfidf.transform(lines).toarray().astype(np.float32)

	out = model(torch.from_numpy(x)).data.numpy()
	out /= np.max(out)
	pred = {}
	for (i, char) in enumerate(chars):
		pred[char] = str(list(out[i]))
	with open('char_pred.json', 'w+') as f:
		json.dump(pred, f)


def calc_r2():
	model, lookup, unlabeled, xs, ys, tfidf = train_model()
	ave = ys.mean(axis = 0)
	stot = np.sum((ys - ave)**2, axis = 0)
	x_tensor = torch.from_numpy(xs)
	pred = model(x_tensor).data.numpy()
	sreg = np.sum((pred - ave)**2, axis = 0)
	return 1 - sreg / stot


if __name__ == '__main__':
	# model, lookup, unlabeled, x_train, y_train, tfidf = train_model()
	# print(calc_r2())
	predict()










import torch
import torch.nn as nn
import numpy as np
import json
import collections

ignore = ['.', '!', '?']
MIN_OCCURENCE = 10
learning_rate = 1e-2
regularization = 1e-4
num_epoch = 5000

def get_train_data():
	char_five = '../../data/personality/all_characters.json'
	char_lines1 = '../../data/all_character_lines.json'
	char_lines2 = '../../data/char_quotes.json'

	with open(char_five) as f: ja = json.load(f)
	with open(char_lines1) as f: jl = json.load(f)
	with open(char_lines2) as f: jl2 = json.load(f)

	for c in jl2:
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
	counts = collections.defaultdict(int)
	for line in lines:
		for w in line.split(' '):
			counts[w] += 1
	words = list(filter(lambda k: counts[k] > MIN_OCCURENCE, counts.keys()))

	lookup = {}
	for i, w in enumerate(words):
		lookup[w] = i
	n, d = len(lines), len(words)
	x_train = np.zeros((n, d), dtype = np.float32)
	y_train = big_five
	for (i, line) in enumerate(lines):
		for w in line.split(' '):
			if w in lookup:
				x_train[i, lookup[w]] += 1
	# import pdb; pdb.set_trace()
	invalid = np.sum(x_train, axis = 1) == 0
	x_train /= np.sum(x_train, axis = 1).reshape(n, 1)
	
	x_train[invalid] = 0

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
	return model, lookup, unlabeled

def predict():
	model, lookup, unlabeled = train_model()
	chars = unlabeled.keys()
	n, d = len(unlabeled), len(lookup)
	x = np.zeros((n, d), dtype = np.float32)
	for (i, char) in enumerate(chars):
		for w in unlabeled[char].split(' '):
			if w in lookup:
				x[i, lookup[w]] += 1

	invalid = np.sum(x, axis = 1) == 0
	x /= np.sum(x, axis = 1).reshape(n, 1)	
	x[invalid] = 0

	out = model(torch.from_numpy(x)).data.numpy()
	# import pdb; pdb.set_trace()
	pred = {}
	for (i, char) in enumerate(chars):
		pred[char] = str(list(out[i]))
	with open('char_pred.json', 'w+') as f:
		json.dump(pred, f)

if __name__ == '__main__':
	predict()









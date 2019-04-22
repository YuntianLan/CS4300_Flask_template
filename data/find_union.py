import json
import numpy as np
import Levenshtein

char_five = 'personality/all_characters.json'
char_lines = 'all_character_lines.json'

with open(char_five) as f: ja = json.load(f)
with open(char_lines) as f: jl = json.load(f)

la = list(map(lambda s: s.replace('_', ' ').replace('-', ' '), ja.keys()))
ll = list(map(lambda s: s.replace('_', ' ').replace('-', ' '), jl.keys()))

d = {}
for c in la:
	dists = list(map(lambda s: Levenshtein.distance(s, c), ll))
	idx = np.argmin(dists)
	d[c] = (ll[idx], dists[idx])
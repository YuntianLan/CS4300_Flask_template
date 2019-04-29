import json

with open('cornell_movie_characters.json') as f:
	jc = json.load(f)
with open('char_pred.json') as f:
	jp = json.load(f)

for c in jp:
	if not c in jc:
		print(c)
		continue
	lst = map(float, jp[c][1:-1].split(', '))
	jc[c]['big_five'] = lst

with open('cornell_movie_characters_bigfive.json', 'w+') as f:
	json.dump(jc, f)
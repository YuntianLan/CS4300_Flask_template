from helpers import *
import random

m = Matcher()
s = set()

for i in range(int(1e7)):
	lst = [random.randint(1, 7) for _ in range(10)]
	names, _, _, _, _, _ = m.match(lst)
	for nm in names: s.add(nm)
	if i % 10000 == 0:
		print('%f percent done' % (i * 100 / 1e7))
		print(len(s))
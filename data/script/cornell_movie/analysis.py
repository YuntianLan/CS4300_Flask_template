import matplotlib.pyplot as plt
import collections

movies = []

with open('movie_titles_metadata.txt', 'r') as f:
    for line in f:
        movies.append(map(lambda s: s.strip(), line.split('+++$+++')))

d = {}
for m in movies:
    mid, name, year, rate, votes, types = m
    mid = int(mid[1:])
    year = int(year[:4])
    rate = float(rate)
    votes = int(votes)
    types = map(lambda s: s.strip(), types.split(','))
    types[0] = types[0][1:]
    types[-1] = types[-1][:-1]
    types = map(lambda s: s[1:-1], types)
    sd = {}
    sd['year'] = year
    sd['rate'] = rate
    sd['votes'] = votes
    sd['types'] = types
    d[mid] = sd

gd = collections.defaultdict(int)
for md in d.values():
    for nm in md['types']:
        gd[nm] += 1

gnere = gd.keys()
lst = []
for i in range(len(gnere)):
    lst += [i] * gd[gnere[i]]

plt.subplot(2,1,1)
plt.hist(map(lambda s: s['year'], d.values()))
plt.title('Production Year Count')
plt.xlabel('Year')

plt.subplot(2,1,2)
sth1, bins, sth2 = plt.hist(lst, bins = len(gnere) - 1)
plt.xticks(bins, gnere)
plt.title('Gnere Count')
plt.xlabel('Gnere')

plt.show()
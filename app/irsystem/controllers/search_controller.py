from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import Matcher
import numpy as np


FANDOMS = ["got", "hp", "mar", "sw", "other"]

matcher = Matcher()

@irsystem.route('/', methods=['GET', 'POST'])
def index():
	return render_template('search.html')

@irsystem.route('/result', methods=['GET'])
def result():
	query = [int(request.args.get('group%d' % i)) for i in range(10)]
	adj = request.args.get('adj', '')
	catchphrase = request.args.get('catchphrace', '')
	char = request.args.get('character', '')

	fandoms = []
	for i, f in enumerate(FANDOMS):
		if request.args.get(f)=="yes":
			fandoms.append(i)


	res = matcher.match(query, fandoms, adj, catchphrase, char)
	cnames, mnames, quotes, urls, vecs, user_vec = res
	cnames_under = [cname.replace(" ","_") for cname in cnames]

	return render_template('result.html',
		user_vec = user_vec,

		char1=cnames[0], char1under=cnames_under[0], movie1=mnames[0], vec1=vecs[0],
		quote1=quotes[0][0].split('\n'), saidby1=quotes[0][1], url1=urls[0],

		char2=cnames[1], char2under=cnames_under[1], movie2=mnames[1], vec2=vecs[1],
		quote2=quotes[1][0].split('\n'), saidby2=quotes[1][1], url2=urls[1],

		char3=cnames[2], char3under=cnames_under[2], movie3=mnames[2], vec3=vecs[2],
		quote3=quotes[2][0].split('\n'), saidby3=quotes[2][1], url3=urls[2],

		char4=cnames[3], char4under=cnames_under[3], movie4=mnames[3], vec4=vecs[3],
		quote4=quotes[3][0].split('\n'), saidby4=quotes[3][1], url4=urls[3],

		char5=cnames[4], char5under=cnames_under[4], movie5=mnames[4], vec5=vecs[4],
		quote5=quotes[4][0].split('\n'), saidby5=quotes[4][1], url5=urls[4],
	)


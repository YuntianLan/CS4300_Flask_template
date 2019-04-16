from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import Matcher
import numpy as np

pname = "Who are you on screen?"
net_id = ""

matcher = Matcher()

@irsystem.route('/', methods=['GET', 'POST'])
def search():
	return render_template('search.html', name=pname, netid=net_id)

@irsystem.route('/result', methods=['GET'])
def result():
	print(request.args)
	query = [
		int(request.args.get('group0')),
		int(request.args.get('group1')),
		int(request.args.get('group2')),
		int(request.args.get('group3')),
		int(request.args.get('group4')),
		int(request.args.get('group5')),
		int(request.args.get('group6')),
		int(request.args.get('group7')),
		int(request.args.get('group8')),
		int(request.args.get('group9'))
	]
	cnames, mnames, quotes, vecs, user_vec = matcher.match(query)

	return render_template('result.html', \
		char1 = cnames[0], movie1 = mnames[0], quote1 = quotes[0],\
		vec1 = vecs[0], user_vec = user_vec)

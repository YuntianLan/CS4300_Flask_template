from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import Matcher
import numpy as np

project_name = "Who are you on screen?"
net_id = ""

matcher = Matcher()

@irsystem.route('/', methods=['POST'])
def search():
	# if not request.args.get('questionOne'):
	# 	return render_template('search.html', \
	# 		name = project_name, netid = net_id)

	query = [
		int(request.get_json('group0')),
		int(request.get_json('group1')),
		int(request.get_json('group2')),
		int(request.get_json('group3')),
		int(request.get_json('group4')),
		int(request.get_json('group5')),
		int(request.get_json('group6')),
		int(request.get_json('group7')),
		int(request.get_json('group8')),
		int(request.get_json('group9')),
	]
	cnames, mnames, quotes, vecs, user_vec = matcher.match(query)

	return render_template('result.html', \
		char1 = cnames[0], movie1 = mnames[0], quote1 = quotes[0],\
		vec1 = vecs[0], user_vec = user_vec)




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
		vec1 = vecs[0], user_vec = user_vec,
		char2=cnames[1], movie2=mnames[1], vec2=vecs[1], quote2=quotes[1],
		char3=cnames[2], movie3=mnames[2], vec3=vecs[2], quote3=quotes[2],
		char4=cnames[3], movie4=mnames[3], vec4=vecs[3], quote4=quotes[3],
		char5=cnames[4], movie5=mnames[4], vec5=vecs[4], quote5=quotes[4]
	)


@irsystem.route('/index', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@irsystem.route('/scriptmatch', methods=['GET', 'POST'])
def beh():
	return render_template('scriptmatch.html')



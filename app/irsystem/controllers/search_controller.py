from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import Matcher

project_name = "Who are you on screen?"
net_id = ""

matcher = Matcher()

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	data = [1,2,3,4,5] # why the fuck do I need this???
	if not query:
		output_message = ''
	else:
		query = list(map(float, query.split(',')))
		res = matcher.match(query)
		output_message = "" + res
	return render_template('search.html', \
		name=project_name, netid=net_id, \
		output_message=output_message, data=data)




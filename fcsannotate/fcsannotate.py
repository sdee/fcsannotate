import tempfile, os, sys
from datetime import datetime
from flask import Flask, send_file, request, abort
from fcsparser.fcsparser.api import FCSParser
from utils import create_temporary_copy

app = Flask(__name__)

def annotate_file(filepath, cytometer='iQue_1', **custom_experimental_metadata):
	#first, make sure file is a valid FCS file
	try:
		fp = FCSParser(filepath)
	except ValueError as value_error:
		raise value_error
	annotations = fp.annotation.copy()
	#match the format of the timestamp in the data file format for FCS 3.1
	annotations['labeled_at'] = '{:%d-%b-%Y %H:%M:%S}'.format(datetime.now()).upper()
	annotations['flow_cytometer'] = cytometer
	#add other experimental metadata if present
	for key in custom_experimental_metadata.keys():
		if key.startswith('$'):
			raise ValueError("Cannot change {} in metadata because '$' denotes a standard FCS keyword, and standard FCS keywords cannot be overriden.".format(key))
	annotations.update(custom_experimental_metadata)
	output = os.path.join(tempfile.gettempdir(), 'fcs_output')
	fp.annotation = annotations
	fp.write_to_file(output)
	return output

@app.route('/fcs_data/annotate/', methods=['PUT'])
def annotate_endpoint():
	input_data = request.get_data()
	if not input_data:
		abort(404) #resource not found
	fpath = create_temporary_copy(input_data)
	try:
		output = annotate_file(fpath)
	except:
		abort(500)
	if (os.path.exists(fpath)):
		os.remove(fpath)
	return send_file(output)

if __name__ == '__main__':
	app.run()

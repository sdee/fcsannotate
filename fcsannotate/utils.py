import os, tempfile

def create_temporary_copy(data):
	temp_dir = tempfile.gettempdir()
	temp_path = os.path.join(temp_dir, 'temp_file_name')
	with open(temp_path, 'wb') as f:
		f.write(data)
	return temp_path

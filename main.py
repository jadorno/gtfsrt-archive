import datetime as dt
import requests
import tarfile
import pytz
import sys
import os

PB_INPUT_DIR = "pb"
TAR_OUTPUT_DIR = "tar"
delete_after_compress = True

config = {}

if os.environ.get('API_URL') is not None:
	config['API_URL'] = os.environ.get('API_URL')

	parameters = {'source':os.environ.get('DATASET')}

	req = requests.get(config['API_URL']+"/status/config/name", params=parameters, timeout=10).json()
	config['DATA_NAME'] = os.environ.get('DATA_NAME', req['result'])
	req = requests.get(config['API_URL']+"/status/config/timezone", params=parameters, timeout=10).json()
	config['TIMEZONE'] = os.environ.get('TIMEZONE', req['result'])
	config['PATH_PB'] = os.environ.get('PATH_PB', PB_INPUT_DIR)
	config['PATH_TAR'] = os.environ.get('PATH_TAR', TAR_OUTPUT_DIR)
else:
	config['DATA_NAME'] = os.environ.get('DATA_NAME')
	config['TIMEZONE'] = os.environ.get('TIMEZONE')
	config['PATH_PB'] = os.environ.get('PATH_PB', PB_INPUT_DIR)
	config['PATH_TAR'] = os.environ.get('PATH_TAR', TAR_OUTPUT_DIR)

tz = pytz.timezone(config['TIMEZONE'])

def notify(text):
#	if os.environ.get('API_URL') is not None:
#		payload = { 'header':{ 'timestamp' : int(dt.datetime.now(tz).timestamp()), 'tool' :'task-archive'}, 'data': text }
#		parameters = {'source':os.environ.get('DATASET')}
#		r = requests.post(os.environ.get('API_URL')+"/status/log/insert", params=parameters, json=payload)
	print(text)

notify("Archive Task Started for "+config['DATA_NAME'])

out_arrays = {}

for file in os.listdir(config['PATH_PB']):
	if file.endswith(".pb") or file.endswith(".proto"):

		timestamp = dt.datetime.fromtimestamp(float(file.split("_")[0]), tz)

		out_file_name = config['DATA_NAME']+"-"+timestamp.strftime("%G-Week-%V")
		try:
			out_arrays[out_file_name].append(os.path.join(config['PATH_PB'], file))
		except KeyError:
			out_arrays[out_file_name] = []
			out_arrays[out_file_name].append(os.path.join(config['PATH_PB'], file))

exclude_week = config['DATA_NAME']+"-"+dt.datetime.now(tz).strftime("%G-Week-%V")

for filename, files in sorted(out_arrays.items()):
	
	if filename != exclude_week:
		print(filename+" "+str(len(files))+" files")

		output_file = os.path.join(config['PATH_TAR'], filename+".tar.gz")
		notify("Creating: "+output_file)

		if not os.path.isfile(output_file):
			with tarfile.open(os.path.join(config['PATH_TAR'], filename+".tar.gz"), "w:gz") as tar:
				for file in files:
					tar.add(file)
			if delete_after_compress:
				for file in files:
					os.remove(file)
					print("Removed "+file)
		else:
			notify(output_file+" already exists. This shouldn't be happening.")
		#	print(files)
		#	exit()
	else:
		print(filename+".tar.gz not generated. Week ongoing.")

notify("Archive Task Finished")
import datetime as dt
import requests
import tarfile
import pytz
import sys
import os

input_directory = os.environ.get('PATH_PB')
output_directory = os.environ.get('PATH_TAR')
r = requests.get(os.environ.get('API_URL')+"/status/timezone")
dataset_timezone = r.json()['timezone']
r = requests.get(os.environ.get('API_URL')+"/status/name")
dataset_name = r.json()['name']
tz = pytz.timezone(dataset_timezone)
delete_after_compress = False

out_arrays = {}

for file in os.listdir(input_directory):
	if file.endswith(".pb") or file.endswith(".proto"):

		timestamp = dt.datetime.fromtimestamp(float(file.split("_")[0]), tz)

		out_file_name = dataset_name+"-"+timestamp.strftime("%Y-Week-%V")
		try:
			out_arrays[out_file_name].append(os.path.join(input_directory, file))
		except KeyError:
			out_arrays[out_file_name] = []
			out_arrays[out_file_name].append(os.path.join(input_directory, file))

exclude_week = dataset_name+"-"+dt.datetime.now(tz).strftime("%Y-Week-%V")

for filename, files in sorted(out_arrays.items()):
	
	if filename != exclude_week:
		print(filename+" "+str(len(files))+" files")

		output_file = os.path.join(output_directory, filename+".tar.gz")
		print("Creating: "+output_file)

		if not os.path.isfile(output_file):
			with tarfile.open(os.path.join(output_directory, filename+".tar.gz"), "w:gz") as tar:
				for file in files:
					tar.add(file)
			if delete_after_compress:
				for file in files:
					os.remove(file)
					print("Removed "+file)
		else:
			print(output_file+" already exists. This shouldn't be happening.")
			exit()
	else:
		print(filename+".tar.gz not generated. Week ongoing.")


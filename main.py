from pathlib import Path
import datetime as dt
from tqdm import tqdm
import subprocess
import requests
import zipfile
import shutil
import pytz
import os
import json


data_path = Path('/usr/src/data')

config = None
with open(data_path.joinpath('dataset.json')) as json_file:
    config = json.load(json_file)
tz = pytz.timezone(config['timezone'])

print("Job Started")

exclude_week = config['data_name']+"-GTFSRT-"+dt.datetime.now(tz).strftime("%G-%V")
gtfsrt_path = data_path.joinpath('gtfsrt')
json_path = data_path.joinpath('gtfsrt-json')

for item in gtfsrt_path.iterdir():
	print(item)
	if item.is_dir() and ''.join(item.suffixes) in ['.pb'] and item.stem != exclude_week:

		destination = item.with_suffix('.pb.zip')
		print('Creating', destination.name)
		p = subprocess.run(['7z','a','-tzip', destination, item,'-mx7'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, check=True)

		zip_ok = True
		zip = zipfile.ZipFile(destination, 'r')
		with tqdm(total=len(zip.namelist())) as pbar:
			for feed in item.iterdir():
				if feed.is_dir():
					for feed_item in feed.iterdir():

						with open(feed_item, mode='rb') as uncompressed:
							compressed_path = feed_item.relative_to(gtfsrt_path)
							with zip.open(str(compressed_path)) as compressed:
								if uncompressed.read() != compressed.read():
									zip_ok = False
									break
								else:
									pbar.update()
		zip.close()
		if zip_ok:
			print('Zip Verified. Removing Directory.')
			shutil.rmtree(item)
		else:
			print('Zip Mismatch')
			print(p.stdout)
			exit()

for item in json_path.iterdir():
	print(item)
	if item.is_dir() and ''.join(item.suffixes) in ['.json'] and item.stem != exclude_week:

		destination = item.with_suffix('.json.zip')
		print('Creating', destination.name)
		p = subprocess.run(['7z','a','-tzip', destination, item,'-mx7'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, check=True)

		zip_ok = True
		zip = zipfile.ZipFile(destination, 'r')
		with tqdm(total=len(zip.namelist())) as pbar:
			for feed in item.iterdir():
				if feed.is_dir():
					for feed_item in feed.iterdir():

						with open(feed_item, mode='rb') as uncompressed:
							compressed_path = feed_item.relative_to(json_path)
							with zip.open(str(compressed_path)) as compressed:
								if uncompressed.read() != compressed.read():
									zip_ok = False
									break
								else:
									pbar.update()
		zip.close()
		if zip_ok:
			print('Zip Verified. Removing Directory.')
			shutil.rmtree(item)
		else:
			print('Zip Mismatch')
			print(p.stdout)
			exit()


print("Job Finished")
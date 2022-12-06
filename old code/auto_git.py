#!/usr/bin/env python3
import os
import time

while True:
	try:
		os.system("git pull origin > temp")

		#file = open("temp")
		#text = file.read().strip()

		#if text != "Already up to date.":
		#	os.system("sudo fuser -k 8000/tcp")
		#	os.system("gunicorn -c gunicorn_config.py Founders.wsgi")
	except:
		pass
	finally:
		#os.remove("temp")
		time.sleep(30)

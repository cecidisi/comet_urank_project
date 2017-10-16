#!/usr/bin/env python

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read in file
with open('comet_urank_project/settings.py', 'r') as file:
	filedata = file.read()

# Replce target string
filedata = filedata.replace('DEBUG = True', 'DEBUG = False')

# Write file again
with open('comet_urank_project/settings.py', 'w') as file:
	file.write(filedata)

print 'Set DEBUG = False in settings for production mode'
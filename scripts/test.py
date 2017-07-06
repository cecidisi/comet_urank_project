# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import urllib2
from bs4 import BeautifulSoup as bs
from conf_navigator.models import *
import unicodedata

def test():
	print('This is a test script')
	text = u"“userâ??s”, ‘users’"
	print text
	print isinstance(text, str)
	text2 = text.replace(u'\u201c', '"').replace(u'\u201d', '"').replace("‘", "'").replace("’", "'").replace(u'\xe2??', "'") # smart double quotes
		# .replace('“','"').replace('”','"').replace(u'\xe2??', "'")
	text2 = unicodedata.normalize('NFKD', text2).encode('ascii','ignore')
	print text2
	print isinstance(text2, str)

	text3 = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
	print text3
	print isinstance(text3, str)
	
    


def run():
    test()
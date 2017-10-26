
from upmc.db_connector import *
from upmc.search import *
import time


def run():
	# ES vs DB Search
	# tmsp1 = time.time()
	# articles = DBconnector.get_articles()
	# tmsp1 = time.time() - tmsp1
	# print_green('DB retrieval time = ' + str(tmsp1))

	# tmsp2 = time.time()
	# articles = eSearch.get_all_articles()
	# tmsp2 = time.time() - tmsp2
	# print_green('ES retrieval time = ' + str(tmsp2))
	# print articles[0]

	# # ES Search with increasing amount of fields
	# tmsp = time.time()
	# res = eSearch.search_by_keywords(['migrain'])
	# print_green('Query 1: Matched ' + str(len(res)) + ' results (' + str(time.time() - tmsp) + ')')

	# tmsp = time.time()
	# res = eSearch.search_by_keywords(['migrain'], keywords = True)
	# print_green('Query 2: Matched ' + str(len(res)) + ' results (' + str(time.time() - tmsp) + ')')

	# tmsp = time.time()
	# res = eSearch.search_by_keywords(['migrain'], keywords = True, text_positions = True)
	# print_green('Query 3: Matched ' + str(len(res)) + ' results (' + str(time.time() - tmsp) + ')')

	eSearch.create_year_aggregation()
	# eSearch.get_year_facets()
	
	

	

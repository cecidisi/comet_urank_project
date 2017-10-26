from itertools import groupby
from upmc.models import *
from helper.bcolors import *

def run():
	PubmedYearFacet.objects.all().delete()
	articles = Article.objects.all()
	year_facets = create_year_facets(articles)
	save_year_facets(year_facets)
	print_green('Saved ' + str(len(year_facets)) + ' year facets')


def create_year_facets(articles):
	year_facets = {}
	count_no_year = 0

	year_facets = [(year, len(list(group))) for year, group \
		in groupby(sorted(articles, key=lambda a: a.pub_details.year), lambda a: a.pub_details.year) if year is not None]
	year_facets = sorted(year_facets, key=lambda f: f[0])
	return year_facets



def save_year_facets(year_facets):
	for f in year_facets:
		yf = PubmedYearFacet(year = f[0], count = f[1])
		yf.save()
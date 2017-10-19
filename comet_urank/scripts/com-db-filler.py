from bs4 import BeautifulSoup

from rest_api.models import Colloquium, CleanCol
from rest_api.serializers import ColloquiumSerializer, CleanColSerializer



def add_clean_detail():
    colloquia = Colloquium.objects.all()
    for col in colloquia:
        # cid = col.col_id
        try:
            cc = CleanCol.objects.get(pk=col.col_id) #.update(detail_all = BeautifulSoup(col.detail).text)
            cc.detail_all = BeautifulSoup(col.detail).text
            cc.save()
            print('+++ Added detail_all for col_id = ' + str(col.col_id))
        except CleanCol.DoesNotExist:
        	print('--- No entry for col_id = ' + str(col.col_id))

        
def run():
    add_clean_detail()







from django.core.exceptions import ObjectDoesNotExist
import re
from nltk import word_tokenize
from comet_urank.models import *



def create_usertags():
    print('*** Deleting usertags and usetags_col')
    Usertag.objects.all().delete()

    users = Userinfo.objects.all()
    for user in users:
        userprofile = Userprofile.objects.filter(user_id=user.user_id)
        tags = dict()
        for up in  userprofile:
            if up.usertags:
                tokens = word_tokenize(up.usertags)
                tokens = [t.lower() for t in tokens  if t.isalpha()]
                for tag in tokens:
                    if tag not in tags:
                        tags[tag] = { 'count': 0, 'appears_in' : list(), 'proxtags' : tokens[:] }
                        tags[tag]['proxtags'].remove(tag)
                    if tag in tags:
                        tags[tag]['count'] +=1
                        tags[tag]['appears_in'].append(up.col_id)

        for tag, item in tags.iteritems():
            usertag = Usertag(tag=tag, count=item['count'], user=user)
            usertag.save()
            # print('Saved usertag "' + tag +'" ,id = ' + str(usertag.pk))
            print(usertag)

            for col_id in item['appears_in']:
                cv = Colvideo.objects.filter(colloquium_id=col_id)
                if len(cv):
                    usertag.colvideos.add(cv[0])
                    print('\tSaved relationship with colvideo = ' + str(cv[0].pk))
                    # col = Colloquium.objects.get(pk=col_id)
                    # usertag.colloquia.add(col)
        print('=============================')

        # Usertags need to eb saved before we can link them to one another
        for tag, item in tags.iteritems():
            usertag = Usertag.objects.filter(tag=tag).filter(user_id=user.user_id)[0]
            for proxtag in item['proxtags']:
                proxusertag = Usertag.objects.filter(tag=proxtag).filter(user_id=user.user_id)[0]
                usertag.proxusertags.add(proxusertag)
                print('\t\tAdded realtionship between "' + usertag.tag + '" and "' + proxusertag.tag + '"')






def run():
    create_usertags()

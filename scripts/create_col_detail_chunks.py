import nltk.data
import re
import unicodedata
from rest_api.models import ColText, ColDetailChunk

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')


def create_col_detail_chunk():
    print('************* CREATING ColDetailChunks ***************')
    ColDetailChunk.objects.all().delete()
    tot = 0
    colt = ColText.objects.all()#[:1]

    for c in colt:
        # print('**************************************************************************')
        text = c.detail_clean #.encode('ascii','ignore').replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
        # print('RAW TEXT -->' + text)
        # split_text = text.replace('\t', '').split('\n')   #
        split_text = text.replace('\t', '').splitlines()
        split_text = [t for t in split_text if t]
        # print('====== split text ===========')
        # print(split_text)
        i = 0
        
        for line in split_text:
            sentences = sent_detector.tokenize(line) 
            for s in sentences:
                i = i + 1
                cdc = ColDetailChunk(sentence_original=s, sentence_parsed=s, pos=i, fcol_id=c.fcol_id)
                cdc.save()
                # print('***** Line ' + str(i) + '-->' + s)
                tot = tot + 1
        print('Lines saved for col_id ' + str(c.fcol_id) + ' = ' + str(i))
                
    print('Total ColText entries = ' + str(len(colt)))
    print('Total ColDetailChunk entries = ' + str(tot))
    print('Average = ' + str(tot / len(colt)))



def test():
    # texts  = ['Candidate Machine Learning Department\n\nThesis Proposal \n\n\nAbstract: Graphs appear in a wide range of settings, such as computer networks, the world wide web, biological networks, social networks (MSN/FaceBook/LinkedIn) and many more.',
    # '\na panel discussion with media scholars Alexandra Juhasz (Pitzer College, Media Studies): \u201cTo Teach, Write, and Learn on YouTube: Publishing Theory and Practice On-Line,\u201d and Noah Wardrip-Fruin (University of California, Santa Cruz, Computer Science): \u201cGames About People\u201d\n\r\n\tThe advent of digitally-mediated and networked technologies allowing user representation has led to the emergence of a variety of forms of communication.']
    texts = ['\nLine 1.\n\nLine2\nDr. Smith\n\nMr. No one',
    '\r\n\tAbstract The Navier-Stokes equations describe how the velocity field of a viscous fluid evolves in time.']
    for text in texts:
        print('**************************************************************************')
        print(text)
        # print(text.replace('\t', '').split('\n'))
        split_text = text.replace('\t', '').splitlines()
        split_text = [t for t in split_text if t]
        print('+++++++++++++++++++++++++++++++++')
        print(split_text)
        print('+++++++++++++++++++++++++++++++++')
        # text = text.replace('.\n', ' ').replace('\n', '. ').replace('\r', ' ').replace('\t', ' ')
        # print(text)
        # sentences = split_into_sentences(text)  
        for line in split_text:
            sentences = sent_detector.tokenize(line)
            for s in sentences:
                print('*** Line -->' + s)


def run():
    create_col_detail_chunk()
    # test()

# if __name__ == "__main__":
#     test()





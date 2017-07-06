def run():
	test()

'''			
**********	TEST Keyword extraction	***********
'''

def test():
	talk = Talk.objects.get(pk=4271)
	print talk.title
	# print talk.abstract
	title_tokens = _get_tokens(talk.title)
	# abstract_tokens = _get_tokens(talk.abstract)
	print title_tokens['filtered']
	pos_title = _get_kw_pos_in_text(talk.title, title_tokens['filtered'], title_tokens['stemmed'])


def _get_tokens(text):
		# Tokenize
		tokens = word_tokenize(text)
		tokens = [t.lower() for t in tokens if t.isalpha()]
		tagged = nltk.pos_tag(tokens)
		# Filter and Stem
		filtered = []
		stemmed = []
		for t in tagged:
			# print t[0] + ' = ' + t[1] + '; lemm =  ' + wnl.lemmatize(t[0])
			if t[1] == 'NN':
				filtered.append(t[0])
				stemmed.append(stemmer.stem(t[0]))
			elif t[1] == 'NNS':
				# Add term as is (plural)
				filtered.append(t[0])
				# Lemmatize then stem
				stemmed.append(stemmer.stem(wnl.lemmatize(t[0]))) 
		# Stem
		# stemmed = [stemmer.stem(t) for t in filtered]
		return { 'raw': tokens, 'filtered': filtered, 'stemmed': stemmed }


# def _get_kw_pos_in_text(text, filtered, stemmed):
def _get_kw_pos_in_text(text, filtered, stemmed):
	positions = {}
	word = ''
	for i, ch in enumerate([c for c in str(text)+'.']):
		if ch.isalpha():
			word += ch
		else:
			print '+++ ' + word
			if word.lower() in filtered:
				idx = filtered.index(word.lower())
				stem = stemmed[idx]
				# print 'stem = ' + stem
				if stem not in positions:
					positions[stem] = []
				from_i = i - len(word)
				to_i = i
				positions[stem].append({
					'from': from_i,  #i,
					'to': to_i       #i + len(word)
				}) 
				print 'stem = ' + stem
				print 'from: '+ str(from_i) +', to: ' + str(to_i)
				print 'testing --> ' + text[from_i:to_i]
			word = ''
	return positions
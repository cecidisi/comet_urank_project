var extend = require("extend");
var path = require('path');
var _ = require('underscore');
var natural = require('../libs/natural/index.js');
var Tagger = natural.BrillPOSTagger;
var logger = require('winston');

var KeywordExtractor2 = (function () {

	var STR_UNDEFINED = 'undefined';
	var _this,
	s = {},
	//stemmer,
	tokenizer, nounInflector, TfIdf, tfidf, stopWords, 
	pos,
	lexer,
	tagger,
	POS = {
		NN : 'NN', // singular noun
		NNS : 'NNS', // plural noun
		NNP : 'NNP', // proper noun
		JJ : 'JJ', // adjective
		VB : 'VB', // verb, base form          eat
		VBD : 'VBD', //verb, past tense        ate
		VBG : 'VBG', //verb, gerund            eating
		VBN : 'VBN', //verb, past part         eaten
		VBP : 'VBP', //Verb, present           eat
		VBZ : 'VBZ' //Verb, present           eats
	};

	//  CONSTRUCTOR
	function KeywordExtractor2(arguments) {
		s = extend({
				minDocFrequency : 2,
				minRepetitionsInDocument : 1,
				maxKeywordDistance : 3,
				minRepetitionsProxKeywords : 4,
				freqAdjectives: 0.05
			}, arguments);
		_this = this;
		this.collection = [];
		this.documentKeywords = [];
		this.collectionKeywords = [];
		this.collectionKeywordsDict = {};
		this.customWords = ['unsupervised', 'supervised', 'semi'],
		this.tokenLogs = { NN: [], NNP: [], NNS: [], VBG: [], JJ: [] };		
		// Attach Porter stemmer
		natural.PorterStemmer.attach();
		tokenizer = new natural.WordTokenizer();
		nounInflector = new natural.NounInflector();
		nounInflector.attach();
		//tfidf = new natural.TfIdf(),
		stopWords = natural.stopwords;
		TfIdf = natural.TfIdf;
		// pos = new Pos();
		// lexer = new pos.Lexer();
		// tagger = new pos.Tagger();
		

	}

	/************************************************************************************************************************************
	 *
	 *   PRIVATE METHODS
	 *
	 ************************************************************************************************************************************/

	var extractDocumentKeywords = function (/*collection, */docs) {
		//POS tagging
		for(var i=0, len=docs.length; i<len; i++) {
			docs[i].taggedWords = tagger.tag(tokenizer.tokenize(docs[i].text));
		}
		// Find out which adjectives are potentially important and worth keeping
		var keyAdjectives = getKeyAdjectives(docs);
		// Create each item's document to be processed by tf*idf
		for(var i=0, len=docs.length; i<len; i++) {
			docs[i].tokens = getFilteredTokens(docs[i].taggedWords, keyAdjectives); // d.tokens contains raw nouns and important adjectives							
			tfidf.addDocument(docs[i].tokens.map(function (token) {	return token.stem(); }).join(' ')); // string of stemmed terms in document array
		}
		// Save keywords for each document
		var documentKeywords = [];
		for(var i=0, len=docs.length; i<len; i++) {
			var terms = tfidf.listTerms(i), obj = {};
			for(var j=0, len2=terms.length; j<len2; j++) {
				var item = terms[j];
				if (isNaN(item.term) && parseFloat(item.tfidf) > 0) {
					obj[item.term] = item.tfidf;
				}
			}
			documentKeywords.push(obj);
		}
		return documentKeywords;
	};

	var getKeyAdjectives = function (_collection) {		
		var candidateAdjectives = [], keyAdjectives = [];
		logger.log('info', 'keywordExtractor2: LET\'S FIND SOME ADJECTIVES');
		_collection.forEach(function (d, i) {
			// Find out which adjectives are potentially important and worth keeping
			d.taggedWords.forEach(function (tw) {
				if (tw[1] == POS.JJ || tw[1] == POS.VBD) {
					var adjIndex = _.findIndex(candidateAdjectives, function (ca) { return ca.adj === tw[0].toLowerCase() });
					if (adjIndex == -1) {
						candidateAdjectives.push({ 'adj' : tw[0].toLowerCase(), 'repeated' : 1 });
					} else {
						candidateAdjectives[adjIndex].repeated++;
					}
				}
			});
		});
		var minRepetitions = parseInt(_collection.length * s.freqAdjectives);
		logger.log('info', 'keywordExtractor2: Candidate Adjectives = ' + candidateAdjectives.length);
		logger.log('info', 'keywordExtractor2: min repetitions = ' + minRepetitions);
		
		candidateAdjectives.forEach(function (ca) {
			if (ca.repeated >= minRepetitions || _this.customWords.elementIn(ca)) {
				keyAdjectives.push(ca.adj);
			}
		});
		logger.log('info', 'keywordExtractor2: Frequent Adjectives = ' + keyAdjectives.length);
		return keyAdjectives;
	}

	// Filter out meaningless words, keeping only nouns (plurals are singularized) and key adjectives
	var getFilteredTokens = function (taggedWords, keyAdjectives) {		
		var filteredTerms = [];
		var verbInflector = new natural.PresentVerbInflector();
		
		for(var k=0,len=taggedWords.length; k<len; k++) {			
			var tw = taggedWords[k];
			switch (tw[1]) {
				case POS.NN: // singular noun
					tw[0] = (tw[0].isAllUpperCase() && !tagger.lexicon[tw[0].toLowerCase()]) ? tw[0] : tw[0].toLowerCase();	// word not lowercased if it'is uppercase and no lexicon entry for lowercased word
					if(stopWords.elementNotIn(tw[0].toLowerCase())) {
						filteredTerms.push(tw[0]);
						if(_this.tokenLogs[POS.NN].indexOf(tw[0]) === -1) _this.tokenLogs[POS.NN].push(tw[0]);
					}					
					break;
				case POS.NNS: // plural noun
					var altPOs = tagger.lexicon[tw[0].toLowerCase()];
					var singular = tw[0].toLowerCase().singularizeNoun();
					if(stopWords.elementNotIn(singular)) {
						filteredTerms.push(singular);						
						if(_this.tokenLogs[POS.NNS].elementNotIn(tw[0]+ ' -> ' + singular)) _this.tokenLogs[POS.NNS].push(tw[0]+ ' -> ' + singular);
					}														
					break;
				case POS.NNP: // proper noun
					var lowerCasedTerm = tw[0].toLowerCase();
					var altEntry = (tagger.lexicon[lowerCasedTerm]) ? tagger.lexicon[lowerCasedTerm] : null;
					if(altEntry) {
						if(altEntry.elementIn(POS.NN) && stopWords.elementNotIn(lowerCasedTerm)) {
							filteredTerms.push(lowerCasedTerm);
							if(_this.tokenLogs[POS.NNP].elementNotIn(tw[0]+' -> '+lowerCasedTerm)) _this.tokenLogs[POS.NNP].push(tw[0]+' -> '+lowerCasedTerm);
						} else if(altEntry.elementIn(POS.NNS) && stopWords.elementNotIn(lowerCasedTerm.singularizeNoun())) {
							filteredTerms.push(lowerCasedTerm.singularizeNoun());
							if(_this.tokenLogs[POS.NNP].elementNotIn(tw[0]+' -> '+lowerCasedTerm.singularizeNoun())) _this.tokenLogs[POS.NNP].push(tw[0]+' -> '+lowerCasedTerm.singularizeNoun());
						}
					} else {
						filteredTerms.push(tw[0]);
						if(_this.tokenLogs[POS.NNP].elementNotIn(tw[0]) === -1) _this.tokenLogs[POS.NNP].push(tw[0]);
					}					
					// tw[0] = (tagger.lexicon[tw[0].toLowerCase()]) ? tw[0].toLowerCase().singularizeNoun() : tw[0];					
					// filteredTerms.push(tw[0]);
					break;
				case POS.VBD:
				case POS.JJ:					
					if (keyAdjectives.elementIn(tw[0]) && stopWords.elementNotIn(tw[0])) {
						filteredTerms.push(tw[0]);
						if(_this.tokenLogs[POS.JJ].elementNotIn(tw[0])) _this.tokenLogs[POS.JJ].push(tw[0]);
					}
					break;
				case POS.VBG:	// -ing verbs
					tw[0] = tw[0].toLowerCase();
					var altPOS = tagger.lexicon[tw[0]];						
					if(altPOS && altPOS.length && altPOS.elementIn(POS.NN) && stopWords.elementNotIn(tw[0])) {
						filteredTerms.push(tw[0].toLowerCase());
						if(_this.tokenLogs[POS.VBG].elementNotIn(tw[0])) _this.tokenLogs[POS.VBG].push(tw[0]);
					}
					break;
				default:
					if(_this.customWords.elementIn(tw[0])) {
						filteredTerms.push(tw[0]);
						if(_this.tokenLogs[POS.JJ].elementNotIn(tw[0])) _this.tokenLogs[POS.JJ].push(tw[0]);
					}
			}
		}
		return filteredTerms;
	}


	/////////////////////////////////////////////////////////////////////////////

	var extractCollectionKeywords = function (collection, documentKeywords, minDocFrequency) {

		minDocFrequency = minDocFrequency ? minDocFrequency : s.minDocFrequency;
		var keywordDict = getKeywordDictionary(collection, documentKeywords, minDocFrequency);

		// get keyword variations (actual terms that match the same stem)
		collection.forEach(function (d, i) {
			d.tokens.forEach(function (token) {
				var stem = token.stem();
				if (keywordDict[stem] && stopWords.indexOf(token.toLowerCase()) == -1) {
					keywordDict[stem].variations[token] = keywordDict[stem].variations[token] ? keywordDict[stem].variations[token] + 1 : 1;
				}
			});
		});
		
		// compute keywords in proximity
		keywordDict = computeKeywordsInProximity(collection, keywordDict);
		var collectionKeywords = [];	
		
		_.keys(keywordDict).forEach(function (keyword, i) {
			// Put keywords in proximity in sorted array
			var proxKeywords = [];
			_.keys(keywordDict[keyword].keywordsInProximity).forEach(function (proxKeyword) {
				var proxKeywordsRepetitions = keywordDict[keyword].keywordsInProximity[proxKeyword];
				if (proxKeywordsRepetitions >= s.minRepetitionsProxKeywords)
					proxKeywords.push({
						stem : proxKeyword,
						repeated : proxKeywordsRepetitions
					});
			});
			keywordDict[keyword].keywordsInProximity = proxKeywords.sort(function (proxK1, proxK2) {
					if (proxK1.repeated < proxK2.repeated)
						return 1;
					if (proxK1.repeated > proxK2.repeated)
						return -1;
					return 0;
				});

			// reverse stemming to get human-readable term
			keywordDict[keyword].term = getRepresentativeTerm(keywordDict[keyword]);
			// if(Object.keys(keywordDict[keyword].variations).length > 2) {
				// console.log('stem = ' + keywordDict[keyword].stem + ' -- term = ' + keywordDict[keyword].term);
				// console.log(keywordDict[keyword].variations);
			// }
			// store each key-value in an array
			if (keywordDict[keyword].term != "ERROR_NO_VARIATIONS") {
				collectionKeywords.push(keywordDict[keyword]);
			}
		});

		// sort keywords in array by document frequency
		collectionKeywords = collectionKeywords.sort(function (k1, k2) {
			if (k1.repeated < k2.repeated) return 1;
			if (k1.repeated > k2.repeated) return -1;
			return 0;
		});
		collectionKeywords.forEach(function (k, i) {
			keywordDict[k.stem].index = i;
		});

		return {
			array : collectionKeywords,
			dict : keywordDict
		};
	};

	var getKeywordDictionary = function (_collection, _documentKeywords, _minDocFrequency) {

		var keywordDict = {};
		_documentKeywords.forEach(function (docKeywords, i) {

			_.keys(docKeywords).forEach(function (stemmedTerm) {
				if (!keywordDict[stemmedTerm]) {
					keywordDict[stemmedTerm] = {
						stem : stemmedTerm,
						term : '',
						repeated : 1,
						variations : {},
						inDocument : [_collection[i].id],
						keywordsInProximity : {}
					};
				} else {
					keywordDict[stemmedTerm].repeated++;
					keywordDict[stemmedTerm].inDocument.push(_collection[i].id);
				}
			});
		});

		_.keys(keywordDict).forEach(function (keyword) {
			if (keywordDict[keyword].repeated < _minDocFrequency)
				delete keywordDict[keyword];
		});
		return keywordDict;
	};

	var computeKeywordsInProximity = function (_collection, _keywordDict) {
		_collection.forEach(function (d) {
			d.tokens.forEach(function (token, i, tokens) {

				var current = token.stem();
				if (_keywordDict[current]) { // current word is keyword

					for (var j = i - s.maxKeywordDistance; j <= i + s.maxKeywordDistance; j++) {
						var prox = tokens[j] ? tokens[j].stem() : STR_UNDEFINED;

						if (_keywordDict[prox] && current != prox) {
							//var proxStem = prox.stem();
							_keywordDict[current].keywordsInProximity[prox] = _keywordDict[current].keywordsInProximity[prox] ? _keywordDict[current].keywordsInProximity[prox] + 1 : 1;
						}
					}
				}
			});
		});
		return _keywordDict;
	};

	var getRepresentativeTerm = function (k) {

		var keys = _.keys(k.variations);

		if (keys.length == 0)
			return "ERROR_NO_VARIATIONS";
		// Only one variations
		if (keys.length == 1)
			return keys[0];
		// 2 variations, one in lower case and the other starting in uppercase --> return in lower case
		if (keys.length == 2 && !keys[0].isAllUpperCase() && !keys[1].isAllUpperCase() && keys[0].toLowerCase() === keys[1].toLowerCase())
			return keys[0].toLowerCase();
		// One variation is repeated >= 70%
		var repetitions = 0;
		for (var i = 0; i < keys.length; ++i)
			repetitions += k.variations[keys[i]];
		for (var i = 0; i < keys.length; ++i)
			if (k.variations[keys[i]] >= parseInt(repetitions * 0.7))
				return keys[i];
		// One variation ends in '-ion', '-ment', '-ism' or '-ty'
		for (var i = 0; i < keys.length; ++i)
			if (keys[i].match(/ion$/) || keys[i].match(/ment$/) || keys[i].match(/ism$/) || keys[i].match(/ty$/))
				return keys[i].toLowerCase();
		// One variation matches keyword stem
		if (k.variations[k.stem])
			return k.stem;
		// Pick shortest variation
		var shortestTerm = keys[0];
		for (var i = 1; i < keys.length; i++) {
			if (keys[i].length < shortestTerm.length)
				shortestTerm = keys[i];
		}
		return shortestTerm.toLowerCase();
	};

	/********************************************************************************************************************************************
	 *
	 *   PROTOTYPE
	 *
	 *********************************************************************************************************************************************/

	KeywordExtractor2.prototype = {
		addDocument : function (document, id) {
			document = (!Array.isArray(document)) ? document : document.join(' ');
			id = id || this.collection.length;
			this.collection.push({
				id : id,
				text : document
			});
			//logger.log('info', 'keywordExtractor2: ' addDocument: '+ JSON.stringify(keywords));
		},
		processCollection : function (onError, onSuccess) {
			logger.log('info', 'keywordExtractor2: Processing ' + _this.collection.length + ' documents ...');
			var timestamp = Date.now();
			var base_folder = path.resolve("../../nodejs/uRank/libs/natural/lib/natural/brill_pos_tagger/data/English");
			var rules_file = base_folder + "/tr_from_posjs.txt";
			var lexicon_file = base_folder + "/lexicon_from_posjs.json";
			var default_category = 'N';
			tfidf = new TfIdf();
			tagger = new Tagger(lexicon_file, rules_file, default_category, function(error) {
				if (error) { 
					onError(error);
				}
				else {					
					_this.documentKeywords = extractDocumentKeywords(_this.collection);
					var colKeywords = extractCollectionKeywords(_this.collection, _this.documentKeywords);
					_this.collectionKeywords = colKeywords.array;
					_this.collectionKeywordsDict = colKeywords.dict;
					
					timestamp = Date.now() - timestamp;
					logger.log('info', 'keywordExtractor2: Extraction finished in ' + (parseInt(timestamp/1000)) + ' seconds, ' + (timestamp%1000) + ' miliseconds (=' + timestamp + ' ms)');
					logger.log('info', 'keywordExtractor2: Total keywords = ' + _this.collectionKeywords.length);
					
					onSuccess({						
						keywords: _this.collectionKeywords,
						keywordsDict: _this.collectionKeywordsDict,
						keywordsList: _this.documentKeywords,
						tokenLogs: _this.tokenLogs
					});
				}
			});
		},
		getListDocumentKeywords : function () {
			return this.documentKeywords;
		},
		listDocumentKeywords : function (index) {
			return this.documentKeywords[index];
		},
		getCollectionKeywords : function () {
			return this.collectionKeywords;
		},
		getCollectionKeywordsDictionary : function () {
			return this.collectionKeywordsDict;
		},
		clear : function () {
			tfidf = null;
			this.collection = [];
			this.documentKeywords = [];
			this.collectionKeywords = [];
			this.collectionKeywordsDict = {};
		}
	};

	return KeywordExtractor2;
})();

module.exports = KeywordExtractor2;
import nltk
from nltk.corpus import stopwords

custom_stopwords = ['research', 'professor', 'university', 'work', 'institute', 'group', 'school', 'center', 
		'program', 'webinar', 'association', 'event', 'field', 'discuss', 'editor', 'share', 'response', 'committee',
		'example', 'challenge', 'review', 'staff', 'opportunity','registration', 'effort', 'provide', 'chairman',
		'faculty', 'speaker', 'management', 'focus', 'way', 'bio', 'office', 'laboratory', 'approach', 'lecture',
		'present', 'member', 'please', 'author', 'chair', 'poster', 'level', 'fellow', 'visit', 'lunch','cover',
		'workshop', 'methodology', 'introduce', 'amount', 'answer', 'youll', 'deliver', 'chapter', 'shift',
		'attend', 'disclaimer', 'appointment', 'involvement', 'become', 'employ', 'moreover', 'definition', 
		'difficulty', 'schedule', 'attempt', 'extend', 'extension', 'scholar', 'anyone', 'everyone', 'start',
		'advisor', 'january', 'bring', 'mentor', 'deputy', 'begin', 'extent', 'consider', 'briefly',
		'highlight', 'apply', 'insight', 'taught', 'paper', 'prefer', 'analysis', 'correct', 'depend', 'manage',
		'challenge', 'mode', 'unit', 'reveal', 'objective', 'half', 'consideration', 'confirm', 'whereas', 'wherea',
		'percentage', 'question', 'versus', 'across', 'demonstrate', 'need', 'author', 'previous', 'finding',
		'majority', 'implication', 'part', 'indication', 'term', 'hour', 'value', 'side', 'confidence', 'response',
		'determine', 'assessment', 'article', 'show', 'literature', 'function', 'outcome', 'level', 'area', 'feature',
		'score', 'conclusion', 'development', 'criteria', 'type', 'test', 'evaluation', 'model', 'method', 'condition',
		'evidence', 'case', 'data', 'study', 'impact', 'addition', 'administration', 'people', 'index', 'performance',
		'release', 'attention', 'importance', 'approaches', 'cost', 'contrast', 'series', 'relevant', 'reason',
		'observation', 'inclusion', 'lack', 'limitation', 'interest', 'significance', 'initiation', 'respond',
		'record', 'sign', 'standard', 'help', 'retrospective', 'hypothesis', 'endpoint', 'threshold', 'represent',
		'solution', 'discussion', 'provide', 'projection', 'suggest', 'guideline', 'affect', 'mild', 'none', 'purpose',
		'decade', 'science', 'phenomenon', 'understand', 'world', 'publication', 'source', 'perspective', 'choice',
		'discovery', 'centre', 'variety', 'avoid', 'validation', 'concept', 'effort', 'delivery', 'step', 'degree',
		'possibility', 'unit', 'preparation', 'category', 'concern', 'requirement', 'center', 'admission', 'input', 
		'description', 'rise', 'direction', 'brief', 'chance', 'consensus', 'subset', 'origin', 'position', 
		'nevertheless', 'advantage', 'offer', 'detail', 'utility', 'line', 'domain', 'individual', 'correction',
		'aim', 'process', 'number', 'result', 'duration', 'use', 'may', 'april', 'therefore', 'characteristic',
		'OBJECTIVE', 'OBJECTIVES', 'CONCLUSION', 'METHODS', 'RESULTS', 'and', 'hence', 'reviewer', 'place',
		'style', 'emphasis', 'today', 'pass', 'current', 'agreement', 'referral', 'rationale', 'average',
		'default', 'opinion', 'success', 'copyright', 'version', 'percent', 'researcher', 'introduction',
		'furthermore', 'respect', 'depends', 'regardless', 'exist', 'likelihood', 'background', 'form',
		'contribution', 'account'
		]


stopwords_list = set(nltk.corpus.stopwords.words('english') + custom_stopwords)
stopwords = { word: True for word in stopwords_list }

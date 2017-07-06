/*
Copyright (c) 2011, Chris Umbel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// a list of commonly used words that have little meaning and can be excluded
// from analysis.
var words = [
    'about', 'after', 'all', 'also', 'am', 'an', 'and', 'another', 'any', 'are', 'as', 'at', 'be',
    'because', 'been', 'before', 'being', 'between', 'both', 'but', 'by', 'came', 'can',
    'come', 'could', 'did', 'do', 'each', 'for', 'from', 'get', 'got', 'has', 'had',
    'I', 'he', 'have', 'her', 'here', 'him', 'himself', 'his', 'how', 'if', 'in', 'into',
    'is', 'it', 'like', 'make', 'many', 'me', 'might', 'more', 'most', 'much', 'must',
    'my', 'never', 'now', 'of', 'on', 'only', 'or', 'other', 'our', 'out', 'over',
    'said', 'same', 'see', 'should', 'since', 'some', 'still', 'such', 'take', 'than',
    'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'those',
    'through', 'to', 'too', 'under', 'up', 'very', 'was', 'way', 'we', 'well', 'were',
    'what', 'where', 'which', 'while', 'who', 'with', 'would', 'you', 'your',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '$', '1',
    '2', '3', '4', '5', '6', '7', '8', '9', '0', '_',
	'i', 'ii', 'iii', 'iv', 'v',
	'others', 'copyright', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'first', 'second', 'third', 'fourth', 'fifth', 'minor', 'data', 'left',
	'right', 'sample', /*'analysis',*/ 'test', 'author', 'article', 'day', 'month', 'year', 'decade', 'century', 'least', 'review', 'worst', 'survey', 'study', 'show',
	'paper', 'research', 'researcher', 'end', 'lack', 'detail', 'focus', 'need', 'elsevier', 'Elsevier', 'approach', 'method', 'methodology', /*'technique',*/ 'type', 'situation',
	'rather', 'hypothesis', 'part', 'deal', 'story', 'process', 'return', 'phase', 'finding', 'purpose', 'position', 'explanation', 'evidence', 'hand', 'half',
	'design', 'limitation', 'implication', 'original', 'originality', 'value', 'reason', 'result', 'theory', 'effect', 'publication', 'abstract', 'fact', 'factor',
	'alternative', 'within', /*'view',*/ 'insight', 'range', 'point', 'assumption', 'field', 'majority', 'minority', 'statistic', 'discussion', 'question', 'address',
	'instance', 'aspect', 'actor', 'citation', 'strategy', 'overview', 'cause', 'future', 'retrospective', 'setting', 'outcome', 'measure', 'age', 'number',
	'forecast', 'conclusion', 'motivation',  'literature', 'variable', 'composition', 'phenomenon', 'mechanism', 'log', 'size', 'area', 'self',
	'sector', 'pattern', 'support', 'group', 'challenge', 'focu', 'period', 'attempt', 'report', 'evaluation', 'mean', 'seek', 'regression', 'quantile', 'panel',
	'today', 'example', 'novel', 'account', 'investigation', 'book', 'participant', 'goal', 'characteristic', 'case', 'introduction', 'scenario', 'implementation',
	'domain', 'footstep', 'selection', 'generalization', /*'feedback',*/ 'framework', 'addition', /*'search',*/ 'scale', 'trial', 'issue', 'degree', 'application', 'step',
	'function', 'module', 'state', 'level', 'concept', 'advantage', 'disadvantage', 'representation', 'problem', 'use', 'person', 'source', 'argument', 'essay',
	'notion', 'struggle', 'responsibility', 'response', 'principle', 'moment', 'kind', 'sorce', 'guideline', /*'recommendation',*/ 'rate', 'cas', 'ratio', 'estimate',
	'term', 'percent', 'basis', 'amount', 'indicator', 'utilization', 'ltd', 'amp', 'chapter', 'different', 'difference', 'form', 'importance', 'new', 'fault', 'help',
	'present', 'several', 'few', 'lot', 'work', 'effort', 'reference', 'campus', 'dozen', 'consideration', 'motive', 'key', 'anything', 'something',
	// adjectives
	'important', 'useful', 'recent', 'efficient', 'effective', 'available', 'simple', 'practical', 'current', 'particular', 'specific', 'various', 'possible', 'able', 'due',
	'additionally', 'previous', 'main', 'good',
	// -ing verbs/nouns
	'making', 'performing', 'failing', 'handling', 'understanding', 'viewing', 'focusing', 'fostering', 'becoming', 'covering', 'running', 'giving',
	'monitoring', 'developing', 'missing', 'following', 'leading', 'reasoning', 'higing', 'being', 'undoing', 'managing', 'collecting', 'telling',
	'leaving', 'publishing', 'hiding', 'forming', 'stopping', 'underpinning', 'coping', 'leveraging', 'belonging', 'finishing', 'switching', 
	'reviewing', 'sprouting', 'founding', 'copying', 'listing',
    '__key'
	];
    
// tell the world about the noise words.    
exports.words = words;

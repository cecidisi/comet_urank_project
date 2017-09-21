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

var SingularPluralInflector = require('./singular_plural_inflector'),
    util = require('util'),
    FormSet = require('./form_set');

function attach() {
    var inflector = this;
    
    String.prototype.singularizeNoun = function() {
        return inflector.singularize(this);
    }
    
    String.prototype.pluralizeNoun = function() {
        return inflector.pluralize(this);
    }
}

var NounInflector = function() {
    this.ambiguous = [
        'bison', 'bream', 'carp', 'chassis', 'cod', 'corps', 'debris', 'deer',
        'diabetes', 'equipment', 'elk', 'fish', 'flounder', 'gallows', 'graffiti',
        'headquarters', 'herpes', 'highjinks', 'homework', 'information',
        'mackerel', 'mews', 'money', 'news', 'rice', 'rabies', 'salmon', 'series',
        'sheep', 'shrimp', 'species', 'swine', 'trout', 'tuna', 'whiting', 'wildebeest'
    ];
    
    this.customPluralForms = [];
    this.customSingularForms = [];    
    this.singularForms = new FormSet();
    this.pluralForms = new FormSet();

    this.attach = attach;	
	// pre-defined
    this.addIrregular("child", "children");
    this.addIrregular("man", "men");
    this.addIrregular("person", "people");
    this.addIrregular("sex", "sexes");
    this.addIrregular("mouse", "mice");
    this.addIrregular("ox", "oxen");
    this.addIrregular("foot", "feet");
    this.addIrregular("tooth", "teeth");
    this.addIrregular("goose", "geese");
    this.addIrregular("ephemeris", "ephemerides");
	// latin plurals
	this.addIrregular("phenomenon", "phenomena");
	this.addIrregular("antenna", "antennae");
	this.addIrregular("bacterium", "bacteria");
    this.addIrregular("alga", "algae");
	this.addIrregular("amoeba", "amoebae");
	this.addIrregular("cactus", "cacti");
	this.addIrregular("fungus", "fungi");
	this.addIrregular("genus", "genera");
	this.addIrregular("larva", "larvae");
	this.addIrregular("stimulus", "stimuli");
	this.addIrregular("vertebra", "vertebrae");
	this.addIrregular("campus", "campuses");
	// -o becomes -oes
	this.addIrregular("echo", "echoes");
	this.addIrregular("embargo", "embargoes");
	this.addIrregular("hero", "heroes");
	this.addIrregular("tomato", "tomatoes");
	this.addIrregular("potato", "potatoes");
	this.addIrregular("torpedo", "torpedoes");
	this.addIrregular("veto", "vetoes");
	// changing vowel sounds
	this.addIrregular("louse", "lice");
	this.addIrregular("woman", "women");
	// -f becomes -ves
	this.addIrregular("calf", "calves");
	this.addIrregular("elf", "elves");
	this.addIrregular("half", "halves");
	this.addIrregular("hoof", "hooves");
	this.addIrregular("knife", "knieves");
	this.addIrregular("leaf", "leaves");
	this.addIrregular("life", "lives");
	this.addIrregular("loaf", "loaves");
	this.addIrregular("self", "selves");
	this.addIrregular("shelf", "shelves");
	this.addIrregular("thief", "thieves");
	this.addIrregular("wife", "wives");
	this.addIrregular("wolf", "wolves");
	// -is becomes -es
	this.addIrregular("axis", "axes");
	this.addIrregular("analysis", "analyses");
	this.addIrregular("basis", "bases");
	this.addIrregular("crisis", "crises");
	this.addIrregular("diagnosis", "diagnoses");
	this.addIrregular("ellipsis", "ellipses");
	this.addIrregular("emphasis", "emphases");
	this.addIrregular("hypothesis", "hypotheses");
	this.addIrregular("neurosis", "neuroses");
	this.addIrregular("oasis", "oases");
	this.addIrregular("paralysis", "paralyses");
	this.addIrregular("parenthesis", "parentheses");
	this.addIrregular("thesis", "theses");
	this.addIrregular('synapsis', 'synapses');
	// -ix becomes -ices
	this.addIrregular("appendix", "appendices");
	this.addIrregular("index", "indices");
	this.addIrregular("matrix", "matrices");
	// unchanged plurals
	this.addIrregular("barracks", "barracks");
	this.addIrregular("deer", "deer");
	this.addIrregular("fish", "fish");
	this.addIrregular("gallows", "gallows");
	this.addIrregular("means", "means");
	this.addIrregular("offspring", "offspring");
	this.addIrregular("series", "series");
	this.addIrregular("sheep", "sheep");
	this.addIrregular("species", "species");	
	// singular ends in -s or -se or -e
	this.addIrregular("gas", "gases");
	this.addIrregular("bus", "buses");
	this.addIrregular('phase', 'phases');
	this.addIrregular('response', 'responses');
	this.addIrregular('purpose', 'purposes');
	this.addIrregular('tie', 'ties');
	this.addIrregular('lens', 'lenses');
	this.addIrregular('virus', 'viruses');
	this.addIrregular('size', 'sizes');
	// singular ends in -ve  to plural -ves
	this.addIrregular("motive", "motives");
	this.addIrregular('narrative', 'narratives');
	this.addIrregular('objective', 'objectives');
	
	
	
	
    // see if it is possible to unify the creation of both the singular and
    // plural regexes or maybe even just have one list. with a complete list
    // of rules it may only be possible for some regular forms, but worth a shot    
    this.pluralForms.regularForms.push([/y$/i, 'ies']);
    this.pluralForms.regularForms.push([/ife$/i, 'ives']);
    this.pluralForms.regularForms.push([/(antenn|formul|nebul|vertebr|vit)a$/i, '$1ae']);    
    this.pluralForms.regularForms.push([/(octop|vir|radi|nucle|fung|cact|stimul)us$/i, '$1i']);    
    this.pluralForms.regularForms.push([/(buffal|tomat|tornad)o$/i, '$1oes']);    
    this.pluralForms.regularForms.push([/(sis)$/i, 'ses']);
    this.pluralForms.regularForms.push([/(matr|vert|ind|cort)(ix|ex)$/i, '$1ices']);
    this.pluralForms.regularForms.push([/(x|ch|ss|sh|s|z)$/i, '$1es']);
    this.pluralForms.regularForms.push([/^(?!talis|.*hu)(.*)man$/i, '$1men']);
    this.pluralForms.regularForms.push([/(.*)/i, '$1s']);

    this.singularForms.regularForms.push([/([^v])ies$/i, '$1y']);
    this.singularForms.regularForms.push([/ives$/i, 'ife']);
    this.singularForms.regularForms.push([/(antenn|formul|nebul|vertebr|vit)ae$/i, '$1a']);
    this.singularForms.regularForms.push([/(octop|vir|radi|nucle|fung|cact|stimul)(i)$/i, '$1us']);
    this.singularForms.regularForms.push([/(buffal|tomat|tornad)(oes)$/i, '$1o']);
    this.singularForms.regularForms.push([/(analy|naly|synop|parenthe|diagno|the)ses$/i, '$1sis']);
    this.singularForms.regularForms.push([/(vert|ind|cort)(ices)$/i, '$1ex']);
    // our pluralizer won''t cause this form of appendix (appendicies)
    // but we should handle it
    this.singularForms.regularForms.push([/(matr|append)(ices)$/i, '$1ix']);
    this.singularForms.regularForms.push([/(x|ch|ss|sh|s|z)es$/i, '$1']);
    this.singularForms.regularForms.push([/men$/i, 'man']);
    this.singularForms.regularForms.push([/s$/i, '']);
    
    this.pluralize = function (token) {
        return this.ize(token, this.pluralForms, this.customPluralForms);
    };
    
    this.singularize = function(token) {
        // var singular = this.ize(token, this.singularForms, this.customSingularForms);
		// return singular;
		return this.ize(token, this.singularForms, this.customSingularForms);
    };
};

util.inherits(NounInflector, SingularPluralInflector);
    
module.exports = NounInflector;
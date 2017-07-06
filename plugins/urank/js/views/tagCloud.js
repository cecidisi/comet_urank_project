// var $ = require('jquery');
// var _ = require('underscore');
var VIEWS = require('../config/views');


var TagCloud = (function() {

    var _this, $root = $('');
    // Settings
    var s = {};
    //  Classes
    var tagcloudClass = 'urank-tagcloud',
        tagcloudControlsClass = 'urank-tagcloud-controls',
        notFoundClass = 'not-found',
        tagFreqSliderClass = 'urank-tagcloud-freq-slider',
        tagContainerOuterClass = 'urank-tagcloud-tag-container-outer',
        tagClass = 'urank-tagcloud-tag';

    var $tagInput = $(''), $notFoundLabel = $(''), $tagFreqLabel = $(''), $tagFreqSlider = $(''), $outerTagContainer = $(''), minFreq = 0, maxFreq = 0;

    //  Constructor
    function TagCloud(params) {
        _this = this;
        s = $.extend({
            root: '',
            attr: {},
            options: {},
            view : 'default',
            cb:{
                onTagInCloudMouseEnter: function(index){},
                onTagInCloudMouseLeave: function(index){},
                onTagInCloudClick: function(index){},
                onKeywordEntered: function(keyword){},
                onTagFrequencyChanged: function(min, max){},
                onTagClickedChange: function(index){}
            }
        }, params);
        // s.root = '.'+tagContainerOuterClass; // change sub-root

        this.keywords = [];
        this.keywordsDict = {};
        init();
        // Initialize selected tagcloud module
        var tagcloudView = VIEWS.TAGCLOUD[s.options.view];
        var tagcloudConf = _.omit(s, 'view');
        tagcloudConf.root = '.'+tagContainerOuterClass; // change sub-root
        this.tagcloud = new tagcloudView(tagcloudConf);
    }

    function init() {
        // Empty tag container and add appropriateclass
        $root = $(s.root);
        $root.empty().addClass(tagcloudClass);
        //  Create tagcloud controls
        var $tagcloudControls = $('<div/>').appendTo($root).addClass(tagcloudControlsClass);
        $tagFreqLabel = $('<label/>').appendTo($tagcloudControls).addClass('tag-freq');
        $tagFreqSlider = $('<div/>').appendTo($tagcloudControls);

        // Notfound message label
        $notFoundLabel = $('<a/>').appendTo($tagcloudControls);
        // Keyword search input
        $tagInput = $('<input>', { type: 'text', placeholder: 'Enter keyword' }).appendTo($tagcloudControls);
        // Search icon in text input
        $('<a/>').appendTo($tagcloudControls).addClass('search-icon');

        // Create tag container
        $outerTagContainer = $('<div></div>').appendTo($root).addClass(tagContainerOuterClass);
    }

    var onTextEntered = function() {
        var stemmedText = $tagInput.val().stem();
        if(_this.keywordsDict[stemmedText])
            s.cb.onKeywordEntered.call(this, _this.keywordsDict[stemmedText]);
        else
            $notFoundLabel.addClass(notFoundClass);
    };


    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype methods

    /**
    * * @param {array of objects} keywords Description
    */
    var _build = function(keywords, data, colorScale, opt, keywordsDict){

        _this.keywords = keywords;
        _this.keywordsDict = keywordsDict;

        minFreq = _this.keywords[_this.keywords.length - 1].df;
        maxFreq = _this.keywords[0].df;
        $tagFreqLabel.html('Keyword frequency: <strong>' + minFreq + '</strong> - <strong>' + maxFreq + '</strong>');

        $tagFreqSlider.slider({
            range: true,
            animate: true,
            min: minFreq,
            max: maxFreq,
            values: [minFreq, maxFreq],
            slide: function(event, ui) {
                $tagFreqLabel.html('Keyword frequency: <strong>' + ui.values[0] + '</strong> - <strong>' + ui.values[1] + '</strong>');
                s.cb.onTagFrequencyChanged.call(this, ui.values[0], ui.values[1]);
            },
            stop: function(event, ui) {
//                s.onTagFrequencyChanged.call(this, ui.values[0], ui.values[1]);
            }
        });

        // Keyword search input
        $tagInput.autocomplete({
            source: _this.keywords.map(function(k){ return k.term })
        }).off('keyup').on('keyup', function(e){
            $notFoundLabel.removeClass(notFoundClass);
            if(e.keyCode == 13 && $(this).val() != '')
                onTextEntered();
        });

        // // Initialize selected tagcloud module
        // var tagcloudView = s.view; //TAGCLOUD_MODULES[opt.module] || TAGCLOUD_MODULES.default;
        // this.tagcloud = new tagcloudView($.extend(s, { root: '.'+tagContainerOuterClass }));
        this.tagcloud.clear();
        // Build tagcloud module
        //var options = $.extend(opt.misc, { draggableClass: tagClass });
        this.tagcloud.build(keywords, data, colorScale, keywordsDict);
        return this;
    };


    var _reset = function() {
        if(this.tagcloud) this.tagcloud.reset();
        return this;
    };


    var _restoreTag = function(index, id){
        if(this.tagcloud) this.tagcloud.restoreTag(index, id);
        return this;
    };


    var _hoverTag = function(index, id) {
        if(this.tagcloud) this.tagcloud.hoverTag(index, id);
        return this;
    };


    var _unhoverTag = function(index, id) {
        if(this.tagcloud) this.tagcloud.unhoverTag(index, id);
        return this;
    };


    var _tagClicked = function(index, id) {
        if(this.tagcloud) this.tagcloud.tagClicked(index, id);
        return this;
    };

    var _updateClonOfDroppedTag = function(index, id, queryColor) {
        if(this.tagcloud) this.tagcloud.updateClonOfDroppedTag(index, id, queryColor);
        return this;
    };


    var _focusTag = function(keyword) {
        this.tagcloud.focusTag(keyword);
    };

    var _showTagsWithinRange = function(min, max) {
        this.tagcloud.showTagsWithinRange(min, max);
    };

    var _clearEffects = function() {
        if(this.tagcloud) this.tagcloud.clearEffects();
        return this;
    };


    var _clear = function() {

        if(this.tagcloud) {
            $tagFreqSlider.slider('destroy');
            $tagInput.val('').autocomplete('destroy');
            $notFoundLabel.removeClass(notFoundClass);
            $outerTagContainer.empty();
            this.tagcloud.clear();
        }
        return this;
    };


    var _destroy = function() {
        if(this.tagcloud) this.tagcloud.destroy();
        $root.removeClass(tagcloudClass);
        return this;
    };


    TagCloud.prototype = {
        build: _build,
        reset: _reset,
        restoreTag: _restoreTag,
        hoverTag: _hoverTag,
        tagClicked:_tagClicked,
        unhoverTag: _unhoverTag,
        updateClonOfDroppedTag: _updateClonOfDroppedTag,
        focusTag: _focusTag,
        showTagsWithinRange: _showTagsWithinRange,
        clearEffects: _clearEffects,
        clear: _clear,
        destroy: _destroy
    };

    return TagCloud;
})();

module.exports = TagCloud;

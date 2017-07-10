var Globals = require('../config/globals');
var utils = require('../helper/utils');

var TagBox = (function(){

    var _this;
    // Settings
    var s = {};
    //  Classes
    var tagboxClass = 'urank-tagbox',
        tagboxContainerClass = 'urank-tagbox-container',
        clearBtnClass = 'urank-tagbox-clear-btn',
        tagInBoxClass = 'urank-tagbox-tag',
        tagDeleteButtonClass = 'urank-tagbox-tag-delete-button',
        tagWeightsliderClass = 'urank-tagbox-tag-weight-slider',
        weightSliderRangeClass = 'urank-tagbox-tag-weight-slider-range',
        weightSliderHandleClass = 'urank-tagbox-tag-weight-slider-handle',
        rankingModeHeaderClass = 'urank-tagbox-ranking-mode-header',
        rankingModeHeaderInnerClass = 'urank-tagbox-ranking-mode-header-inner',
        headerSectionClass = 'urank-tagbox-ranking-mode-header-section',
        highlightedClass = 'urank-tagbox-ranking-mode-header-highlighted',
        headerStyleClass = 'urank-header-style',
        modeLegendClass = 'urank-ranking-mode-legend',
        legendWeightBar = 'urank-tagbox-ranking-weight-bar';

    //  Id prefixes
    var kwtagIdPrefix = '#urank-tag-';
    var utagIdPrefix = '#urank-usertag-';
    var neighborTagPrefix = '#urank-neighbortag-';
    //  Attribute
    var tagPosAttr = 'tag-pos';
    //  Helpers
    var $root = $(''), 
        $tagContainer, 
        $rankingModeHeader, 
        $splitRankings = $(''), 
        $sumRankings = $(''), 
        $contentHeader, 
        $socialHeader, 
        $resetBtn, 
        $message;

    // Contructor
    function TagBox(params) {
        _this = this;
        s = $.extend({
            root: '',
            options: {
                header: {
                    enabled: false,
                    useHybrid: false,
                    useSplit: false
                },    
                aes :{
                    defaultBlockStyle: true,    
                }
            },
            cb :{
                onModeChanged: function(mode){},
                onRankingWeightChanged: function(rWeight) {},
                onTagDropped: function(arr_index_id){},
                onTagDeleted: function(index, id){},
                onTagWeightChanged: function(index, id, weight){},
                onTagInBoxMouseEnter: function(index, id){},
                onTagInBoxMouseLeave: function(index, id){},
                onTagInBoxClick: function(index, id){},
                onReset: function(){}
            },
            droppableClass: 'urank-tagcloud-tag',
        }, params);

        $root = $(s.root);

        s.ui = {
            // droppable tags
            droppableOptions : {
                tolerance: 'touch',
                drop: function(event, ui){
                    ui.draggable.data('dropped', true);
                    var index = $(ui.draggable).attr('tag-pos');
                    var id = $(ui.draggable).attr('tag-id');
                    // sibling tags for multiple drag
                    var addedTags = ui.draggable.data('addedTags'); 
                    // ui.draggable.data('addedTags').forEach(function(addedTag){
                    //     addedTagIndices.push(addedTag);
                    // });
                    if(addedTags.length) {
                        s.cb.onMultipleTagsSelected($.merge([ 
                            { 'index': index, 'id': id }, //original tag
                            addedTags
                        ]));
                    } else {
                        s.cb.onTagSelected.call(this, index, id);    
                    }
                }
            },
            // tag weight slider
            sliderOptions : {
                orientation: 'horizontal',
                animate: true,
                range: "min",
                min: 0,
                max: 1,
                step: 0.1,
                value: 1,
                start: function(event, ui) {},
                slide: function(event, ui) {
                    var $tag  = $(this.parentNode);
                    var color = $tag.data('queryTermColor');
                    $tag.css("background", "rgba("+ utils.hexToR(color) + ', ' + utils.hexToG(color) + ', ' + utils.hexToB(color) + "," + ui.value + ")");
                },
                stop: function(event, ui) {
                    var index =  $(this.parentNode).attr('tag-pos'),
                        id =  $(this.parentNode).attr('tag-id'),
                        weight = ui.value;
                    s.cb.onTagWeightChanged.call(this, index, id, weight);
                }
            },
            // CB-TU weight slider
            rankingWeightSliderOptions : {
                animate: true,
                //range: 'min',
                min: 0,
                max: 1,
                step: 0.1,
                value: 0.5,
                slide: function(event, ui) {
                    $('.'+legendWeightBar+"[name='CB']").css('background', 'rgba(0,0,0,' + (1 - ui.value) + ')');
                    $('.'+legendWeightBar+"[name='CF']").css('background', 'rgba(0,0,0,' + ui.value + ')');
                },
                stop: function(event, ui) {
                    s.cb.onRankingWeightChanged.call(this, ui.value);
                }
            }    
        };

    }



    var buildRankingModeHeader = function(ranking_conf) {

        $rankingModeHeader = $('<div/>').appendTo($root).addClass(rankingModeHeaderClass);

        // Split rankings
        if(s.options.header.useSplit) {
            $splitRankings = $('<div/>').appendTo($rankingModeHeader)
                .addClass(rankingModeHeaderInnerClass);//.hide();
            // One column per RS 
            ranking_conf.rs.forEach(function(rs) {
                if(rs.active) {
                    $rsHeader = $('<div/>', {id: 'header-'+rs.name }).appendTo($splitRankings)
                        .addClass(headerSectionClass)
                        .on('click', function(evt){ 
                            evt.stopPropagation();
                            s.cb.onModeChanged.call(this, rs.name)
                        });
                    if(rs.name === ranking_conf.rankBy) {
                        $rsHeader.addClass(highlightedClass);
                    }
                $('<div/>', { class: modeLegendClass, text: rs.pretty }).appendTo($rsHeader)
                    .append($('<span/>'));

                }
            });
            // Sum button (add only if useHybrid = true)
            if(s.options.header.useHybrid) {
                $('<button/>', { class: 'my-btn', title: 'Aggregate rankings' }).appendTo($splitRankings)
                    .addClass('sum')
                    .html("<span></span>")
                    .on('click', function(evt){ 
                        evt.stopPropagation();
                        s.cb.onModeChanged.call(this, 'overall') 
                    });
            }
        }

        // Aggregated rankings
        if(s.options.header.useHybrid) {
            $sumRankings = $('<div/>').appendTo($rankingModeHeader)
                .addClass(rankingModeHeaderInnerClass)
                .hide();

            var $sumHeader = $('<div/>').appendTo($sumRankings)
                .addClass(headerSectionClass + ' long ' + highlightedClass)
                // .on('click', function(evt){ 
                //     evt.stopPropagation();
                //     s.cb.onModeChanged.call(this, 'overall') 
                // });

            // header legend
            ranking_conf.rs.forEach(function(rs, i){
                if(rs.active) {
                    //  add grey-shaded square and RS label
                    $('<div/>', { name: rs.name }).appendTo($sumHeader).addClass(legendWeightBar)
                    $('<div/>', { name: rs.anme , text: ' '+rs.pretty+' ' }).appendTo($sumHeader).addClass(modeLegendClass);
                    if(i < ranking_conf.length - 1) {
                        // add plus button in between
                        $('<div/>', { text: ' + ' }).appendTo($sumHeader).addClass(modeLegendClass + ' plus-symbol').html('<span></span>');    
                    }

                    // HARD FIX !! ranking weight slider
                    if(i==0){
                        $('<div/>', { title: "Move left to increase Content Ranking's weight" })
                            .appendTo($sumHeader).slider(s.ui.rankingWeightSliderOptions);
                    }
                }
            });

            // // ranking weight slider
            // $('<div/>', { title: "Move right to increase Content Ranking's weight" })
            //     .appendTo($sumHeader).slider(s.ui.rankingWeightSliderOptions);

            // Split button (show only if useSplit = true)
            if(s.options.header.useSplit) {
                $('<button/>', { title: 'Split rankings' }).appendTo($sumRankings).addClass('split').html("<span></span>")
                    .on('click', function(evt){ 
                        evt.stopPropagation();
                        s.cb.onModeChanged.call(this, 'CB') 
                    });
            }
        }
        _updateRankingMode(ranking_conf.rankBy)
    };




    var _build = function(ranking_conf) {
        this.destroy();
        $root = $(s.root).addClass(tagboxClass);

        var tagboxContainerClasses = (s.options.aes.defaultBlockStyle) ? tagboxContainerClass +' '+ headerStyleClass : tagboxContainerClass;
        $tagContainer = $('<div/>').appendTo($root)
            .addClass(tagboxContainerClasses);
        $tagContainer.droppable(s.ui.droppableOptions);                       // bind droppable behavior to tag box;
        $message = $('<div/>', { class: 'message', html: Globals.STR.DROP_TAGS_HERE}).appendTo($tagContainer);
        $resetBtn = $('<a/>', { href: '#' }).appendTo($tagContainer)
            .addClass(clearBtnClass)
            .on('click', function(){ s.cb.onReset.call(this); }).hide();

        if(!s.options.header.enabled) {
            $tagContainer.addClass('large');
        }
        else {
            buildRankingModeHeader(ranking_conf);
        }
        return this;
    };


    var _clear = function() {
        if($tagContainer) {
            $tagContainer.find('.'+tagInBoxClass).remove();
            //$tagContainer.append('<p>' + STR_DROP_TAGS_HERE + '</p>');
            $message.show();
            $resetBtn.hide();
        }
        //$root.find('.'+tagboxContainerClass).empty().append('<p>' + STR_DROP_TAGS_HERE + '</p>');
        return this;
    };

var getTagPrefix = function(tag){
    if(tag.type === 'keyword')
        return kwtagIdPrefix;
    if(tag.type === 'usertag')
        return utagIdPrefix; 
    if(tag.type === 'neighbor')
        return neighborTagPrefix;
};


/*
    tag = { index, stem, term, color }
*/
    var _appendTag = function(tag){
        var prefix = getTagPrefix(tag)
        var $tag = $(prefix + '' + tag.id + '-clon');

        //if ($tag.hasClass(s.droppableClass)) {
            // Append dragged/clicked tag to tag box, refactor classes
            $tag = $tag.detach().appendTo($tagContainer)
                .removeClass().addClass(tagInBoxClass);
            // Append "delete" button
            $('<span></span>').appendTo($tag).addClass(tagDeleteButtonClass);
            // Add new div to make it a slider
            var weightSlider = $("<div class='" + tagWeightsliderClass + "'></div>").appendTo($tag)
                .slider($.extend(true, s.ui.sliderOptions, {
                    slide: function(event, ui) {
                        // var $tag  = $(this.parentNode);
                        var color = $tag.data('queryTermColor');
                        $tag.css("background", "rgba("+ utils.hexToR(color) + ', ' + utils.hexToG(color) + ', ' + utils.hexToB(color) + "," + ui.value + ")");
                    },
                    stop: function(event, ui) {
                        // var tag ={
                        //     index: $tag.attr('tag-pos'),
                        //     id: $tag.attr('tag-id'),
                        //     weight: ui.value   
                        // };
                        console.log(tag);
                        tag.weight = ui.value
                        s.cb.onTagWeightChanged.call(this, tag);
                    }
                }));
            weightSlider.find('.ui-slider-range')
                .addClass(weightSliderRangeClass)
                .css('background', tag.color);
            weightSlider.find('.ui-slider-handle')
                .addClass(weightSliderHandleClass);
            // Retrieve color in weightColorScale for the corresponding label
            var rgbSequence = utils.hexToR(tag.color) + ', ' + utils.hexToG(tag.color) + ', ' + utils.hexToB(tag.color);
            // Set tag's style
            $tag.data('queryTermColor', tag.color).css({
                background: 'rgba(' + rgbSequence + ', 1)',
                color: '',
                border: 'solid 1px ' + tag.color
            }).off().on({
                mouseenter: s.cb.onTagInBoxMouseEnter(tag.index, tag.id),
                mouseleave: s.cb.onTagInBoxMouseLeave(tag.index, tag.id),
                click: s.cb.onTagInBoxClick(tag.index, tag.id)
            }).on('click', '.'+tagDeleteButtonClass, function(event){  //  Event handler for delete button
                    event.stopPropagation();
                    s.cb.onTagDeleted.call(this, tag);
            });
        //}
        this.refresh();
        return this;
    };


    var _deleteTag = function(tag) {
        // fix identifier
        var prefix = getTagPrefix(tag);
        $(prefix + '' + tag.id + '-clon').remove();
        console.log('Deleted clon of tag with id = ' + tag.id);
        this.refresh();
        return this;
    };

    var _reset = function() {
        // Remove all buttons and sliders
        $('.'+tagDeleteButtonClass).remove();
        $('.'+tagWeightsliderClass).remove();
        return this;
    };

    var _destroy = function() {
        if($(s.root).hasClass(tagboxClass)) {
            $tagContainer.droppable('destroy');
            $root.empty().removeClass(tagboxContainerClass);
        }
        return this;
    };


    var _getHeight = function(){
        return $(s.root).height();
    };


    var _updateRankingMode = function(mode) {
        // FIX!!
        console.log(mode);
        if(mode == 'overall') {
            $splitRankings.hide();
            $sumRankings.show();
        }
        else {
            $splitRankings.show();
            $sumRankings.hide();
            hid = '#header-'+mode;
            console.log(hid);
            $(hid).addClass(highlightedClass);
            $('.'+headerSectionClass).not($(hid)).removeClass(highlightedClass);
        }
        return this;
    };


    var _updateRankingWeight = function(rWeight) {
        console.log($('.'+legendWeightBar+"[name='content']"));
    };


    var _refresh = function(){
        var is_empty = $tagContainer.find('.'+tagInBoxClass).length ? false : true;
        if(is_empty) {
            // $message.show();
            // $resetBtn.hide();
            this.clear();
        }
        else {
            $resetBtn.css('display', '');
            $message.hide();
        }
        return this;
    };

    // Prototype
    TagBox.prototype = {
        build: _build,
        reset: _reset,
        clear: _clear,
        appendTag: _appendTag,      // tag added via drand and drop
        deleteTag: _deleteTag,
        updateRankingMode: _updateRankingMode,
        refresh: _refresh,
        destroy: _destroy,
        getHeight: _getHeight
    };

    return TagBox;
})();


module.exports = TagBox;

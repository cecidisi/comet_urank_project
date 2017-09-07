var DocViewer = (function(){

    var _this;
    // Settings
    var s = {};
    // Classes
    var docViewerOuterClass = 'urank-docviewer-outer',
        docViewerContainerClass = 'urank-docviewer-container',
        defaultDocViewerContainerClass = 'urank-docviewer-container-default',
        detailsSectionClass = 'urank-docviewer-details-section',
        contentSectionOuterClass = 'urank-docviewer-content-section-outer',
        contentSectionClass = 'urank-docviewer-content-section';
    // Id prefix
    var detailItemIdPrefix = '#urank-docviewer-details-';
    // Selectors
    var $root = $(''), $container = $(''), $detailsSection = $(''), $contentSectionOuter = $(''), $contentSection = $('');
    // Helper
    var customScrollOptions = {
        axis: 'y',
        theme: 'light',
        scrollbarPosition: 'outside',
        autoHideScrollbar: true,
        scrollEasing: 'linear',
        mouseWheel: {
            enable: true,
            axis: 'y'
        },
        keyboard: {
            enable: true
        },
        advanced: {
            updateOnContentResize: true
        }
    };



    function DocViewer(params) {
        s = $.extend({
            root: '',
            attr : {},
            options : {
                attrToShow: [],
                aes: {
                    defaultBlockStyle: true,
                    customScrollBars: true,
                    textDecoration: 'background'
                }
            },
            cb : {
                onDocViewerHidden: function(){}  
            } 
        }, params);
        _this = this;
    }


    var _build = function() {

        if(s.root === '') {
            $('.'+docViewerOuterClass).remove();
            $root = $('<div/>').appendTo('body').addClass(docViewerOuterClass).hide();
            $container = $('<div/>').appendTo($root).addClass(docViewerContainerClass);
        }
        else {
            $root = $(s.root).empty();
            $container = $root;
        }

        $root.on('click', function(event){ event.stopPropagation(); s.cb.onDocViewerHidden.call(this); });
        $container.on('click', function(event){ event.stopPropagation() });

        // Append details section, titles and placeholders for doc details
        $detailsSection = $("<div class='" + detailsSectionClass + "'></div>").appendTo($container);

        var $titleContainer = $('<div/>').appendTo($detailsSection);
        $("<label>Title:</label>").appendTo($titleContainer);
        $("<h3 id='urank-docviewer-details-title'></h3>").appendTo($titleContainer);
        // var $authorSection = $('<div/>').appendTo($detailsSection);
        // $('<label/>').appendTo($authorSection).html('Author:');
        // $('<span/>', { id: 'urank-docviewer-details-author' }).appendTo($authorSection);

        s.options.attrToShow.forEach(function(field){
            var field_name = field.attr.replace('.', '-')
            var $fieldContainer = $('<div/>').appendTo($detailsSection);
            if (field.style ) {
                $fieldContainer.addClass(field.style)
            }
            $("<label id='label-'" + field_name + ">" + field.label + ":</label>").appendTo($fieldContainer);
            $("<span id='details-" + field_name + "'></span>").appendTo($fieldContainer);
        });

        // Append content section for snippet placeholder
        $contentSectionOuter = $('<div></div>').appendTo($container).addClass(contentSectionOuterClass);
        $contentSection = $('<div></div>').appendTo($contentSectionOuter).addClass(contentSectionClass);
        $('<p></p>').appendTo($contentSection);

        $root.on('mousedown', function(event){ event.stopPropagation(); });

        //if(s.options.aes.customScrollBars)
            // $contentSectionOuter/*.css('overflowY', 'hidden')*/.mCustomScrollbar(customScrollOptions);
    };


    var addField = function(field, doc){
        var field_name = field.attr.replace('.', '-')
        var attrs = field.attr.split('.')
        var value = doc[attrs[0]]
        for(var j=1; j < attrs.length; j++) {
            value = value[attrs[j]]
        }
        $("#label-" + field_name).html(field.label);
        $("#details-" + field_name).html(value);
    };

    /**
    * @private
    * Description
    * @param {type} document Description
    * @param {Array} keywords (only stems)
    */
    var _showDocument = function(doc, keywords, colorScale){

        $root.show();
        // var title = doc[s.attr.pretty_title] || doc[s.attr.title];
        $(detailItemIdPrefix + 'title').html(doc[s.attr.title]);
        // $(detailItemIdPrefix + 'title').html(getStyledText(doc[s.attr.title], keywords, colorScale));
        // $(detailItemIdPrefix + 'author').html(doc.creator);
        var fields = (s.options && s.options.attrToShow) ? s.options.attrToShow : [];
        fields.forEach(function(field){
            addField(field, doc)
        });

        $contentSection.empty();
        // var $p = $('<p></p>').appendTo($contentSection).html(getStyledText(doc[s.attr.description], keywords, colorScale));
        // var description = doc[s.attr.pretty_description] || doc[s.attr.description];
        var $p = $('<p></p>').appendTo($contentSection).html(doc[s.attr.description]);
        $p.hide().fadeIn('slow').scrollTo('top');
        $contentSectionOuter.mCustomScrollbar('update');
    };


    var _clear = function(){
        $root.hide();
        // Clear details section
        $(detailItemIdPrefix + 'title').empty();
        // $(detailItemIdPrefix + 'author').empty();
        // var facets = (s.options && s.options.attrToShow) ? s.options.attrToShow : [];
        // facets.forEach(function(facet){
        //     $(detailItemIdPrefix + '' + facet).empty();
        // });
        // Clear content section
        $contentSection.empty();
    };


    var _destroy = function() {
        $root.empty().removeClass(docViewerContainerClass)
    };


    // Prototype
    DocViewer.prototype = {
        build: _build,
        clear: _clear,
        showDocument: _showDocument,
        destroy: _destroy
    };

    return DocViewer;
})();


module.exports = DocViewer;

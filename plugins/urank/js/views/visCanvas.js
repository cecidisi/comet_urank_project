var VIEWS = require('../config/views');

var VisCanvas = (function(){

    //  Settings
    var _this, s = {};
    // Classes
    var viscanvasClass = 'urank-viscanvas',
        viscanvasContainerClass = 'urank-viscanvas-container',
        visCanvasMessageClass = 'urank-viscanvas-message',
        hiddenScrollbarClass = 'urank-hidden-scrollbar',
        hiddenScrollbarInnerClass = 'urank-hidden-scrollbar-inner';
    // Helper
    var $root = $(''), $scrollable = $(''), $visContainer = $(''), $visContainerSocial = $('');

    var onScroll = function(event) {
        event.stopPropagation();
        s.cb.onScroll.call(this, _this, $(this).scrollTop());
    };


    function VisCanvas(params) {
        _this = this;
        s = $.extend(true, {
            root: '',
            options : {
                view : 'ranking',
                aes: {
                    lightBackgroundColor: '',
                    darkBackgroundColor: '',
                    hideScrollbar: false
                }
            },
            cb : {
                onItemClicked: function(doc, i){},
                onItemMouseEnter: function(doc, i){},
                onItemMouseLeave: function(doc, i){},
                onScroll: function(caller, scrollTop){}
            }
        }, params);
        init();

        var viscanvasView = VIEWS.VISCANVAS[s.options.view];
        var viscanvasConf = _.omit(s, 'view');
        viscanvasConf.root = '.'+viscanvasContainerClass;
        this.vis = new viscanvasView(viscanvasConf);
    }


    function init(){
        $root = $(s.root).empty().addClass(viscanvasClass);

        //  Set scrolling
        if(s.options.aes.hideScrollbar) {
            $root.addClass(hiddenScrollbarClass);
            $scrollable = $('<div/>').appendTo($root).addClass(hiddenScrollbarInnerClass);
            $scrollable = $root.mCustomScrollbar(customScrollOptions);
        }
        else {
            $scrollable = $root;
        }
        $scrollable.on('scroll', onScroll);
        $visContainer = $('<div/>').appendTo($scrollable).addClass(viscanvasContainerClass);
    };

    var _build = function(data, height) {
        // this.height = height;
        // $root = $(s.root).empty().addClass(viscanvasClass);

        // //  Set scrolling
        // if(opt.misc.hideScrollbar) {
        //     $root.addClass(hiddenScrollbarClass);
        //     $scrollable = $('<div/>').appendTo($root).addClass(hiddenScrollbarInnerClass);
        //     $scrollable = $root.mCustomScrollbar(customScrollOptions);
        // }
        // else {
        //     $scrollable = $root;
        // }
        // $scrollable.on('scroll', onScroll);
        // $visContainer = $('<div/>').appendTo($scrollable).addClass(viscanvasContainerClass).height(this.height);

        // var viscanvasView = opt.view;
        // var visOptions = {
        //     root: '.'+viscanvasContainerClass,
        //     onItemClicked: s.onItemClicked,
        //     onItemMouseEnter: s.onItemMouseEnter,
        //     onItemMouseLeave: s.onItemMouseLeave,
        //     lightBackgroundColor: opt.customOptions.lightBackgroundColor,
        //     darkBackgroundColor: opt.customOptions.darkBackgroundColor,
        // };
        // this.vis = new viscanvasView(visOptions);

        this.height = height;
        $visContainer.height(this.height);
        this.vis.build(data, height);
        return this;
    };


    var _update = function(params) {
        $scrollable.scrollTo('top');
        this.vis.update(params);
        $visContainer.height(this.vis.getHeight());
        return this;
    };

    var _resize = function(listHeight){
        if(this.vis) this.vis.resize(listHeight);
        return this;
    };

    var _clear = function(){
        if(this.vis) this.vis.clear();
    //    $root.append("<p class='" + visCanvasMessageClass + "'>" + STR_NO_VIS + "</p>");
        return this;
    };

    var _reset = function() {
        if(this.vis) this.vis.reset();
        $visContainer.height(this.height);
        return this;
    };

    var _selectItem =function(id, index) {
        if(this.vis) this.vis.selectItem(id, index);
        return this;
    };

    var _deselectAllItems =function() {
        if(this.vis) this.vis.deselectAllItems();
        return this;
    };

    var _hoverItem = function(id, index) {
        if(this.vis) this.vis.hoverItem(id, index);
        return this;
    };

    var _unhoverItem = function(id, index) {
        if(this.vis) this.vis.unhoverItem(id, index);
        return this;
    };

    var _highlightItems = function(idsArray) {
        if(this.vis) this.vis.highlightItems(idsArray);
        return this;
    };

    var _clearEffects = function() {
        if(this.vis) if(this.vis) this.vis.clearEffects();
        $visContainer.css('height', '');
        return this;
    };

    var _destroy = function() {
        if(this.vis) this.vis.clear();
        $root.removeClass(viscanvasClass+' '+hiddenScrollbarClass);
        return this;
    };

    var _scrollTo = function(offset) {
        $scrollable.off('scroll', onScroll)
            .scrollTop(offset)
            .on('scroll', onScroll);
    };


    VisCanvas.prototype = {
        build: _build,
        update: _update,
        clear: _clear,
        reset: _reset,
        resize: _resize,
        selectItem: _selectItem,
        deselectAllItems: _deselectAllItems,
        hoverItem: _hoverItem,
        unhoverItem: _unhoverItem,
        highlightItems: _highlightItems,
        clearEffects: _clearEffects,
        destroy: _destroy,
        scrollTo: _scrollTo
    };

    return VisCanvas;
})();

module.exports = VisCanvas;

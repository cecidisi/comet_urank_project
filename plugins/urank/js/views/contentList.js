var Globals = require('../config/globals');

var ContentList = (function() {

    var _this;
    // Settings
    var s = {};
    // Classes
    var contentListClass = 'urank-list',
        hiddenScrollbarClass = 'urank-hidden-scrollbar',
        hiddenScrollbarInnerClass = 'urank-hidden-scrollbar-inner',
        listContainerClass = 'urank-list-container',
        ulClass = 'urank-list-ul',
        ulPaddingBottomclass = 'urank-list-ul-padding-bottom',
        liClass = 'urank-list-li',
        liLightBackgroundClass = 'urank-list-li-lightbackground',
        liDarkBackgroundClass = 'urank-list-li-darkbackground',
        liUnrankedClass = 'urank-list-li-unranked',
        liMovingUpClass = 'urank-list-li-movingup',
        liMovingDownClass = 'urank-list-li-movingdown',
        liNotMovingClass = 'urank-list-li-notmoving',
        liRankingContainerClass = 'urank-list-li-ranking-container',
        rankingPosClass = 'urank-list-li-ranking-pos',
        rankingPosMovedClass = 'urank-list-li-ranking-posmoved',
        liTitleContainerClass = 'urank-list-li-title-container',
        liTitleClass = 'urank-list-li-title',
        liButtonsContainerClass = 'urank-list-li-buttons-container',
        faviconClass = 'urank-list-li-button-favicon',
        faviconDefaultClass = 'urank-list-li-button-favicon-default',
        watchiconClass = 'urank-list-li-button-watchicon',
        watchiconDefaultClass = 'urank-list-li-button-watchicon-default',
        onClass = 'on',
        offClass = 'off',
        selectedClass = 'selected',
        dimmedClass = 'dimmed',
        hoveredClass = 'hovered',
        watchedClass = 'watched',
        // default-style classes
        ulClassDefault = ulClass + '-default',
        liClassDefault = liClass + '-default',
        // header classes
        headerClass = 'urank-list-header',
        headerPosAndshiftClass = 'urank-list-header-pos-and-shift',
        headerTitleClass = 'urank-list-header-title',
        headerStyleClass = 'urank-header-style';

    // Ids
    var liItem = '#urank-list-li-';

    var urankIdAttr = 'urank-id',
        originalIndex = 'original-index';
    // Helper
    var $root = $(''), $header = $(''), $listContainer = $(''), $scrollable = $(''), $ul = $('');

    var onScroll = function(event){
        event.stopPropagation();
        s.cb.onScroll.call(this, _this, $(this).scrollTop());
    };

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Constructor

    function ContentList(params) {
        _this = this;
        s = $.extend({
            root: '',    
            attr : {},
            options : {},
            cb : {
                onItemClicked: function(documentId, index){},
                onItemMouseEnter: function(documentId, index){},
                onItemMouseLeave: function(documentId, index){},
                onFaviconClicked: function(documentId, indext){},
                onWatchiconClicked: function(documentId, index){},
                onScroll: function(caller, scrollTop){},
                onRatingClicked: function(documentId, index, rating){}
            }
        }, params);

        this.data = [];
        this.selectedKeywords = [];
        this.multipleHighlightMode = false;
    }


    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Internal functions

    var bindEventHandlers = function($li, id, index) {
        var onLiClick = function(event){
            event.stopPropagation();
            hideUnrankedListItems();
            if(!$(this).hasClass(liUnrankedClass))
                s.cb.onItemClicked.call(this, id, index);
        };
        var onLiMouseEnter = function(event){
            event.stopPropagation(); s.cb.onItemMouseEnter.call(this, id, index);
        };
        var onLiMouseLeave = function(event){
            event.stopPropagation(); s.cb.onItemMouseLeave.call(this, id, index);
        };
        var onWatchiconClick = function(event){
            event.stopPropagation();
            s.cb.onWatchiconClicked.call(this, id, index);
        };
        var onFaviconClick = function(event){
            event.stopPropagation();
            // update current state. if class 'on' then new state is 'off'. Class will be toggled later
            state = $(this).hasClass(onClass) ? 'off' : 'on';
            // s.cb.onFaviconClicked.call(this, $li.attr(urankIdAttr), $li.attr(originalIndex), state);
            console.log('Index in content list = ' + index);
            s.cb.onFaviconClicked.call(this, id, index, state);
        };

        $li.off({
            click: onLiClick,
            mouseenter: onLiMouseEnter,
            mouseleave: onLiMouseLeave
        }).on({
            click: onLiClick,
            mouseenter: onLiMouseEnter,
            mouseleave: onLiMouseLeave
        });
        // Fav Icon Event
        $li.find('.'+faviconClass).off().on('click', onFaviconClick);
        // Watch Icon Event
        $li.find('.'+watchiconClass).off().on('click', onWatchiconClick);
    };


    var formatTitles = function(colorScale) {
        _this.data.forEach(function(d, i){
            var title = d[s.attr.title];
            title = (title.length > 80) ? (title.substring(0, 80) + '...') : title;
            formattedTitle = (_this.selectedKeywords.length == 0) ? title : getStyledText(title, _this.selectedKeywords, colorScale);
            $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').find('.'+liTitleClass).html(formattedTitle);
        });
    }


    var updateLiBackground = function(){
        $('.'+liClass).removeClass(liLightBackgroundClass).removeClass(liDarkBackgroundClass).removeClass(liUnrankedClass);

        _this.data.forEach(function(d, i) {
            var backgroundClass = (i % 2 == 0) ? liLightBackgroundClass : liDarkBackgroundClass;
            $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').addClass(backgroundClass);
        });
    };


    // var getColor = function(d) {
    //     if(d.ranking.pos_changed > 0) return "rgba(0, 200, 0, 0.8)";
    //     if(d.ranking.pos_changed < 0) return "rgba(250, 0, 0, 0.8)";
    //     return "rgba(128, 128, 128, 0.8)";
    // };

    // var getPosMoved = function(d) {
    //     if(d.ranking.pos_changed == 1000) return Globals.STR.JUST_RANKED;
    //     if(d.ranking.pos_changed > 0) return "+" + d.ranking.pos_changed;
    //     if(d.ranking.pos_changed < 0) return d.ranking.pos_changed;
    //     return "=";
    // };



    var showRankingPositions = function() {

        var color = function(d) {
            if(d.ranking.pos_changed > 0) return "rgba(0, 200, 0, 0.8)";
            if(d.ranking.pos_changed < 0) return "rgba(250, 0, 0, 0.8)";
            return "rgba(128, 128, 128, 0.8)";
        };

        var posMoved = function(d) {
            if(d.ranking.pos_changed == 1000) return Globals.STR.JUST_RANKED;
            if(d.ranking.pos_changed > 0) return "+" + d.ranking.pos_changed;
            if(d.ranking.pos_changed < 0) return d.ranking.pos_changed;
            return "=";
        };

        _this.data.forEach(function(d, i){
                // if(d.ranking.overall.score ){
                if(d.ranking.pos){
                    try {
                    //var rankingDiv = $(liItem + '' + d[s.attr.id]).find('.'+liRankingContainerClass);
                    var rankingDiv = $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').find('.'+liRankingContainerClass);
                    rankingDiv.css('visibility', 'visible');
                    rankingDiv.find('.'+rankingPosClass).text(d.ranking.pos);
                    rankingDiv.find('.'+rankingPosMovedClass).css('color', color(d)).text(posMoved(d));    
                } catch(e){
                    console.log(e)
                }
                
            }
        });
    };


    var hideUnrankedListItems = function() {

//        if(_this.status !== Globals.RANKING_STATUS.no_ranking) {
//            _this.data.forEach(function(d){
//                var display = d.ranking.total_score > 0 ? '' : 'none';
//                //$(liItem + '' + d[s.attr.id]).css('display', display);
//                $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').css('display', display);
//            });
//            $ul.addClass(ulPaddingBottomclass);
//        }
        _this.multipleHighlightMode = false;
    };


    var removeMovingStyle = function() {
        $('.'+liClass).removeClass(liMovingUpClass).removeClass(liMovingDownClass).removeClass(liNotMovingClass);
    };


    var stopAnimation = function(){
        $('.'+liClass).stop(true, true);
        removeMovingStyle();
        //if(_this.animationTimeout) clearTimeout(_this.animationTimeout);
    };



    var sortList = function(){

        var liHtml = [];
        _this.data.forEach(function(d, i){
            var $current = $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').css('top', '');
            var $clon = $current.clone(true);
            liHtml.push($clon);
            $current.remove();
        });

        $ul.empty();
        liHtml.forEach(function($li){
            $ul.append($li);
            var id = $li.attr(urankIdAttr),
                index = parseInt($li.attr(originalIndex));
            bindEventHandlers($li, id, index);
        });
    };


    var animateAccordionEffect = function() {
        var timeLapse = 50;
        var easing = 'swing';

        $('.'+liClass).each(function(i, item){
            var $item = $(item);
            var shift = (i+1) * 5;
            var duration = timeLapse * (i+1);

            $item.addClass(liMovingUpClass);
            if(i < 40) {
                $item.animate({ top: shift }, 0, easing).queue(function(){
                    $(this).animate({ top: 0 }, duration, easing)
                }).queue(function(){
                    $(this).css('top', '');
                }).dequeue();
            }
        });
    };



    var animateResortEffect = function() {
        var duration = 1000;
        var easing = 'swing';
        var acumHeight = 0;
        var listTop = $ul.position().top;        
        var itemHeight = $ul.find(':first-child').fullHeight();
        var options = [];

        // Compute shifts
        _this.data.forEach(function(d, i) { 
            var shift = 0;
            // if((_this.status === Globals.RANKING_STATUS.new && d.ranking.pos > 0 && d.ranking.pos < 40) ||
            //    (d.ranking.pos > 0 && d.ranking.pos < 30) ||
            //    (d.ranking.prev_pos > 0 && d.ranking.prev_pos < 30)) {
            //     shift = listTop + (d.ranking.prev_pos - d.ranking.pos) * itemHeight - curTop;
            // }
            if(d.ranking.pos > 0 && d.ranking.pos < 30) {
                var curTop = $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]').position().top;
                var prevTop = listTop + (d.ranking.prev_pos - 1) * itemHeight;                
                shift = prevTop - curTop;
            } 
            options.push({
                shift: shift,
                movingClass: (d.ranking.pos_changed > 0) ? liMovingUpClass : 
                    ((d.ranking.pos_changed < 0) ? liMovingDownClass : '')
            });
        });

        //  Animate 
        $('.'+liClass).each(function(i, item){
            var $item = $(item);
            $item.addClass(options[i].movingClass);
            if(options[i].shift !== 0) {
                $item.css('top', options[i].shift +'px')
                .animate({ top: '0px' }, duration, easing, function(){
                    $(this).css('top', '');
                });
            }
        });
    };


    var animateUnchangedEffect = function () {
        var duration = 1000;
        var easing = 'linear';

        _this.data.forEach(function(d, i) {
            //var $item = $(liItem +''+ d[s.attr.id]);
            var $item = $('.'+liClass+'['+urankIdAttr+'="'+d[s.attr.id]+'"]');
            var startDelay = (i+1) * 30;

            setTimeout(function() {
                $item.addClass(liNotMovingClass);
                // item.removeClass(liNotMovingClass, duration, easing);
            }, startDelay);
        });
    };



    var buildCustomList = function() {

        var c = {
            root: s.options.customOptions.selectors.root,
            ul: s.options.customOptions.selectors.ul,
            liClass: s.options.customOptions.selectors.liClass,
            liTitle: s.options.customOptions.selectors.liTitle,
            liRankingContainer: s.options.customOptions.selectors.liRankingContainer,
            watchicon: s.options.customOptions.selectors.watchicon,
            favicon: s.options.customOptions.selectors.favicon,
            liHoverClass: s.options.customOptions.classes.liHoverClass,
            liLightBackgroundClass: s.options.customOptions.classes.liLightBackgroundClass,
            liDarkBackgroundClass: s.options.customOptions.classes.liDarkBackgroundClass,
            hideScrollbar: s.options.customOptions.misc.hideScrollbar
        };

        $ul = $(c.ul).addClass(ulClass);
        $root = $(c.root);

        if(c.hideScrollbar) {
            var $ulCopy = $ul.clone(true);
            $root.empty().addClass(hiddenScrollbarClass);
            $scrollable = $('<div></div>').appendTo($root)
                .addClass(hiddenScrollbarInnerClass)
                .on('scroll', onScroll)
                .append($ulCopy);
            $ul = $('.'+ulClass);
        }
        else {
            $scrollable = $root;
        }

        $(c.liClass).each(function(i, li){
            var $li = $(li),
                id = _this.data[i][s.attr.id];

            $li.addClass(liClass).attr(urankIdAttr, id);
            $li.find(c.liTitle).addClass(liTitleClass);

            var $rankingDiv = $li.find(c.liRankingContainer).empty().addClass(liRankingContainerClass).css('visibility', 'hidden');
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosClass);
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosMovedClass);

            $li.find(c.watchicon).addClass(watchiconClass+' off');
            $li.find(c.favicon).addClass(faviconClass+' off');

            bindEventHandlers($li, id, i);
        });

        hoveredClass = c.liHoverClass == '' ? hoveredClass : c.liHoverClass;
        liLightBackgroundClass = c.liLightBackgroundClass == '' ? liLightBackgroundClass : c.liLightBackgroundClass;
        liDarkBackgroundClass = c.liDarkBackgroundClass == '' ? liDarkBackgroundClass : c.liDarkBackgroundClass;
    };


    var buildDefaultList = function() {

        $root.find('.'+listContainerClass).remove();
        $root.find('.'+hiddenScrollbarInnerClass).remove();

        $listContainer = $('<div/>').appendTo($root).addClass(listContainerClass + ' ' + hiddenScrollbarClass);
        $scrollable = $('<div/>').appendTo($root)
            .addClass(hiddenScrollbarInnerClass)
            .on('scroll', onScroll);

        $ul = $('<ul></ul>').appendTo($scrollable).addClass(ulClass +' '+ ulClassDefault);

        _this.data.forEach(function(d, i) {
            // li element
            var $li = $('<li></li>', { 'urank-id': d[s.attr.id], 'original-index': d.idx || i }).appendTo($ul).addClass(liClass +' '+ liClassDefault);
            // ranking section
            var $rankingDiv = $("<div></div>").appendTo($li).addClass(liRankingContainerClass).css('visibility', 'hidden');
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosClass);
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosMovedClass);
            // title section
            var $titleDiv = $("<div></div>").appendTo($li).addClass(liTitleContainerClass);
            $('<h3></h3>', { id: 'urank-list-li-title-' + i, class: liTitleClass, html: d[s.attr.title]/*, title: d[s.attr.title] + '\n' + d.description*/ }).appendTo($titleDiv);
            // buttons section
            var $buttonsDiv = $("<div></div>").appendTo($li).addClass(liButtonsContainerClass);
            $("<span>").appendTo($buttonsDiv).addClass(watchiconClass+' '+watchiconDefaultClass+' '+offClass);
            var favIconStateClass = d.bookmarked ? onClass : offClass;
            $("<span>").appendTo($buttonsDiv).addClass(faviconClass+' '+faviconDefaultClass+' '+favIconStateClass);
            // Subtle animation
//            $li.animate({ opacity: 0 }, 0)
//                .queue(function(){
//                $(this).animate({ opacity: 1 }, (i+1)*100, 'swing')
//            }).queue(function(){
//                $(this).css('opacity', '');
//                bindEventHandlers($li, d[s.attr.id], i);
//            }).dequeue();
            $li.hide().fadeIn((i+1)*100);
            bindEventHandlers($li, d[s.attr.id], i);
        });
    };


    var buildHeader = function(height){

        $('.'+headerClass).remove();
        $header = $('<div/>').appendTo($root).addClass(headerClass).css('height', height);
        var $headerPos = $('<div/>').appendTo($header).addClass(headerPosAndshiftClass + ' ' + headerStyleClass);
        $('<div/>', { text: 'Position'}).appendTo($headerPos).addClass('label-container');

        var $headerShift = $('<div/>').appendTo($header).addClass(headerPosAndshiftClass + ' ' + headerStyleClass);
        $('<div/>', { text: 'Shift'}).appendTo($headerShift).addClass('label-container');

        var $headerTitle = $('<div/>').appendTo($header).addClass(headerTitleClass + ' ' + headerStyleClass);
        $('<p/>', { text: 'Document Titles'}).appendTo($headerTitle);
    };


    var buildEntries = function(data){
        $ul.empty();
        data.forEach(function(d, i) {
            // li element
            var $li = $('<li></li>', { 'urank-id': d[s.attr.id], 'original-index': i }).appendTo($ul).addClass(liClass +' '+ liClassDefault);
            // ranking section
            var $rankingDiv = $("<div></div>").appendTo($li).addClass(liRankingContainerClass).css('visibility', 'hidden');
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosClass);
            $("<div></div>").appendTo($rankingDiv).addClass(rankingPosMovedClass);
            // title section
            var $titleDiv = $("<div></div>").appendTo($li).addClass(liTitleContainerClass);
            $('<h3></h3>', { id: 'urank-list-li-title-' + i, class: liTitleClass, html: d[s.attr.title]/*, title: d[s.attr.title] + '\n' + d.description*/ }).appendTo($titleDiv);
            // buttons section
            var $buttonsDiv = $("<div></div>").appendTo($li).addClass(liButtonsContainerClass);
            $("<span>").appendTo($buttonsDiv).addClass(watchiconClass+' '+watchiconDefaultClass+' '+offClass);
            var favIconStateClass = d.bookmarked ? onClass : offClass;
            $("<span>").appendTo($buttonsDiv).addClass(faviconClass+' '+faviconDefaultClass+' '+favIconStateClass);
            // $li.hide().fadeIn((i+1)*100);
            bindEventHandlers($li, d[s.attr.id], i);
        });
    };

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype methods

    var _build = function(data, headerHeight) {
        this.originalData = data.slice();
        this.data = data.slice();
        this.selectedKeywords = [];
        this.status = Globals.RANKING_STATUS.no_ranking;
        this.headerHeight = headerHeight || _this.headerHeight;
        $root = $(s.root).addClass(contentListClass);

        if(s.options.header)
            buildHeader(_this.headerHeight);

        if(s.options.custom)
            buildCustomList();
        else
            buildDefaultList();

        formatTitles();
        updateLiBackground();
    };



    /**
    * @private     * Description
    * @param {type} data : current ranking
    * @param {type} status Description
    */
    var _update = function(params) {

        this.status = params.status;
        this.data = params.ranking.length ? params.ranking : this.data;
        
        _this.timestamp = $.now();
        $('.'+liClass).stop(true, true)
            .removeClass(liMovingUpClass).removeClass(liMovingDownClass).removeClass(liNotMovingClass)  //stop animation
            .removeClass(selectedClass).removeClass(dimmedClass);                                        // deselect all classes

        //        console.log('Stop Animation');
        //        stopAnimation();
        //        console.log('Deselect items');
        //        this.deselectAllListItems();
        //        formatTitles(options.colorScale);

        //        console.log('Hide unranked');
        //        hideUnrankedListItems();
        var updateFunc = {};
        updateFunc[Globals.RANKING_STATUS.new] = animateAccordionEffect; //animateResortEffect;
        updateFunc[Globals.RANKING_STATUS.update] = animateResortEffect;
        updateFunc[Globals.RANKING_STATUS.unchanged] = animateUnchangedEffect;
        updateFunc[Globals.RANKING_STATUS.no_ranking] = _this.reset;

        buildEntries(this.data);
        updateLiBackground();
        // sortList();
        console.log(this.status)
        updateFunc[this.status]();
        console.log('In update data.length = ' + this.data.length);
        showRankingPositions();
        setTimeout(removeMovingStyle, 3000);
        //  When animations are triggered too fast and they can't finished in order, older timeouts are canceled and only the last one is executed
        //  (list is resorted according to last ranking state)
    };



    var _reset = function() {
        _this.build(_this.originalData, s.options);
/*        this.data = _this.originalData.slice();
        this.selectedKeywords = [];
        updateLiBackground();
        sortList();
        formatTitles();
        $('.'+liClass).show().find('.'+liRankingContainerClass).css('visibility', 'hidden');

        $ul.removeClass(ulPaddingBottomclass);*/
    };



    var _selectListItem = function(id) {
        stopAnimation();
        $('.'+liClass+'['+urankIdAttr+'!='+id+']').addClass(dimmedClass);
        $('.'+liClass+'['+urankIdAttr+'="'+id+'"]').addClass(selectedClass);
    };


    var _deselectAllListItems = function() {
        $('.'+liClass).removeClass(selectedClass, 1200, 'easeOutCirc').removeClass(dimmedClass);
    };


    // receives actual index
    var _hover = function(id) {
        $('.'+liClass+'['+urankIdAttr+'="'+id+'"]').addClass(hoveredClass);
    };


    var _unhover = function(id) {
        $('.'+liClass+'['+urankIdAttr+'="'+id+'"]').removeClass(hoveredClass);
    };


    var _highlightListItems = function(idArray) {
        stopAnimation();
        $('.'+liClass).each(function(i, li){
            var $li = $(li);
            if(idArray.indexOf($li.attr(urankIdAttr)) === -1)
                $li.addClass(dimmedClass);
//            else {
//                if(!$li.is(':visible'))
//                    $li.removeClass(liDarkBackgroundClass).removeClass(liLightBackgroundClass).addClass(liUnrankedClass);
//                $li.css({ display: '', opacity: ''});
//            }
        });



        $ul.removeClass(ulPaddingBottomclass);
        _this.multipleHighlightMode = true;
    };



    var _clearAllFavicons = function(){
        $('.'+liClass).find(' .' + faviconClass).removeClass(onClass);//.addClass(offClass);
    };


    var _toggleFavicon = function(id, index, state){
        //var favIcon = $(liItem + '' + id).find(' .' + faviconClass);
        var $favIcon = $('.'+liClass+'['+urankIdAttr+'="'+id+'"]').find(' .' + faviconClass);
        var classToAdd = state === 'on' ? onClass : offClass;
        var classToRemove = state === 'on' ? offClass : onClass;
        $favIcon.switchClass(classToRemove, classToAdd);

        if(state === 'on') {
            // background
            $bgCover = $('<div/>', { class: 'bg-cover' }).appendTo($('body'));
            var top = $favIcon.offset().top;
            var left = $favIcon.offset().left;
            console.log(top + ' - ' + left);
            var $rating = $('<div/>', { class: 'tooltip-rating'}).appendTo($('body'));
            $rating.css({
                top: (parseInt(top) - 76) + 'px', 
                left: parseInt(left) + 15 + 'px'
            });
            // .appendTo($favIcon.parent());
            $('<div/>', { class: 'rating-message', html: Globals.LEGENDS.rating }).appendTo($rating);
            var $starContainer = $('<div/>', { class: 'star-container' }).appendTo($rating);
            // append stars
            for(i = 1; i <= 5; i++) {
                var $star = $('<div/>', { class: 'star', id: 'star-'+i, pos: i }).appendTo($starContainer);
                $star.on({
                    mouseover: function(evt) {
                        evt.stopPropagation();
                        var pos = parseInt($(this).attr('pos'));
                        for(j=1; j<=pos; j++) {
                            $('#star-'+j).addClass('hovered');
                        }
                    },
                    mouseleave: function(evt) {
                        evt.stopPropagation();
                        $('.star').removeClass('hovered');
                    },
                    click : function(evt) {
                        evt.stopPropagation();
                        var rating = parseInt($(this).attr('pos'));
                        s.cb.onRatingClicked(id, index, rating)

                        setTimeout(function(){
                            $bgCover.remove();
                            $rating.remove();
                        }, 800);
                    }
                })
            }
        }
    };


    var _toggleWatchListItem = function(id){
        var $li = $('.'+liClass+'['+urankIdAttr+'="'+id+'"]');
        var watchIcon = $li.find(' .' + watchiconClass);
        var classToAdd = watchIcon.hasClass(offClass) ? onClass : offClass;
        var classToRemove = classToAdd === onClass ? offClass : onClass;
        watchIcon.switchClass(classToRemove, classToAdd);
        $li.toggleClass(watchedClass);
    };


    var _clearEffects = function() {
        this.deselectAllListItems();
        if(this.multipleHighlightMode) hideUnrankedListItems();
    };


    var _clear = function() {
        console.log(s.options);
        if(!s.options.custom)
            $root.empty();
        /* todo else */
    };


    var _destroy = function() {
        if(!s.options || !s.options.custom) return;

        if(!s.options.custom)
            $root.empty().removeClass(contentListClass+' '+hiddenScrollbarClass);
        else {
            if($listContainer.hasClass(hiddenScrollbarClass)) {
                var $ulCopy = $ul.clone(true);
                $root.empty().append($ulCopy);
            }
            $root.removeClass(contentListClass);
            $('.'+ulClass).removeClass(ulClass);
            $('.'+liClass).removeAttr(urankIdAttr)
                .removeClass(liClass+' '+liLightBackgroundClass+' '+liDarkBackgroundClass+' '+liUnrankedClass+' '+liMovingUpClass+' '+liMovingDownClass+' '+liNotMovingClass);
            $('.'+liRankingContainerClass).empty().removeClass(liRankingContainerClass);
            $('.'+liTitleClass).removeClass(liTitleClass);
            $('.'+watchiconClass).removeClass(watchiconClass+' '+offClass+' '+onClass);
            $('.'+faviconClass).removeClass(faviconClass+' '+offClass+' '+onClass);
        }
    };


    var _scrollTo = function(scroll) {
        $scrollable.off('scroll', onScroll)
            .scrollTop(scroll)
            .on('scroll', onScroll);
    };

    var _getListHeight = function() {
        return $ul.fullHeight();
    };

    // Prototype
    ContentList.prototype = {
        build: _build,
        reset: _reset,
        update: _update,
        hover: _hover,
        unhover: _unhover,
        selectListItem: _selectListItem,
        deselectAllListItems: _deselectAllListItems,
        highlightListItems: _highlightListItems,
        clearAllFavicons: _clearAllFavicons,
        toggleFavicon: _toggleFavicon,
        toggleWatchListItem: _toggleWatchListItem,
        clearEffects: _clearEffects,
        clear: _clear,
        destroy: _destroy,
        scrollTo: _scrollTo,
        getListHeight: _getListHeight
    };

    return ContentList;
})();

module.exports = ContentList;


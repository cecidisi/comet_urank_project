webpackJsonp([2],[
/* 0 */,
/* 1 */,
/* 2 */,
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var Globals  = {
    STR : {
        NO_VIS : "No visualization yet!",
        DROPPED : "Dropped!",
        DROP_TAGS_HERE : "Drop tags here!",
        JUST_RANKED : "new",
        SEARCHING : "Searching..."//,
        // UNDEFINED : 'undefined'
    },

    RANKING_STATUS : {
        new : 'new',
        update : 'update',
        unchanged : 'unchanged',
        no_ranking : 'no_ranking'
    },

    USER_ACTION : {
        added: 'keyword added',
        deleted: 'keyword deleted',
        weighted: 'changed weight',
        bookmarked: 'document bookmarked',
        unbookmarked: 'document unbookmarked',
        watched: 'watching document',
        unwatched: 'document unwatched',
        mode: 'ranking mode changed'
    },

    LEGENDS: {
        rating: 'How would you rate this item?'
    }
};

module.exports = Globals;

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

var TagCloudDefault = __webpack_require__(19);
var Ranking = __webpack_require__(22);

var VIEWS = {
    VISCANVAS : {
        ranking: Ranking
        // detailedView: DetailedView
    },
    TAGCLOUD : {
        default: TagCloudDefault
    //    ,landscape: LandscapeTagCloud
    }    
};


module.exports = VIEWS;

/***/ }),
/* 5 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(colorbrewer) {
var Config = {
    // ROOT DOM ELEMENTS FOR EACH VIEW
    elem : {
        root: 'body',
        tagCloudRoot: '',
        tagBoxRoot: '',
        contentListRoot: '',
        visCanvasRoot: '',
        docViewerRoot: '',
        usertagBox: '',
        neighborscloudRoot: ''
    },
    features: {
        keywords: true,
        usertags: false,
        neighbors: false
    },
    // NAME OF ATTRIBUTES FOR ID, TITLE, DESCRIPTION. Add url, etc.
    dataAttr : {
        id: 'id',
        title : 'title',
        description : 'description',
        pretty_title: null,
        pretty_description: null
    },
    // RANKING MODEL ON CLIENT SIDE (if isLocal == true)
    rankingModel: {            
        useLocal: true,
        host: '',           // only user if isLocal = false
        rs : [
            {
                name: 'CB',
                active: true,
                weight : 0.5,
                attr : 'keywords',
                pretty: 'Content Ranking'
            },
            {
                name: 'CF',
                active: true,
                weight : 0.5,
                attr : 'neighbors',
                pretty: 'Social Ranking'
            }
        ],
        rankBy : 'CB'   // any RS name or overall
        // rs: {
        //     CB: {
        //         name: 'cb_score',
        //         active: true,
        //         weight : 0.5
        //     },
        //     TU: {
        //         name: 'tu_score',
        //         active: false,
        //         weight : 0.0
        //     },
        //     CF: {
        //         name: 'cf_score',
        //         active: true,
        //         weight: 0.5
        //     },
        //     overall: {
        //         name: 'total_score',
        //         active: true
        //     },
        //     rankBy : 'CB'
        // },
    },
    // VISUAL ARRANGEMENT
    rankingRepresentation: {
        // split_by: 'rs'                  // rs || feature
        split_by: 'feature'                  // rs || feature
    },
    // KEYWORD EXTRACTOR ON CLIENT SIDE
    keywordExtractor: {
        useLocal: true,                 // use client-side keyword extractor or not
        isIncluded: false,           // keywords already present in data
        minDocFrequency: 2,
        minRepetitionsInDocument: 1,
        maxKeywordDistance: 5,
        minRepetitionsProxKeywords: 4,
        excludeStr : {
            url : true,
            contains : []
        }
    },
    // TAG CLOUD (draggable tags)
    tagCloud : {
        view: 'default',              // default || landscape
        numCategories : 5,
        selection: 'click',             // click || drag
        tagStyle: 'word',               // word || badge
        highlight: 'background',        // body || background
        minFontSize : 12,               // in px    
        fontSizeGrowth: 0.1           // minFontSize + fontSizeGrowth * keyword.score (df) 
    },
    // USERTAG BOX
    usertagBox: {
        minFontSize : 9,               // in px    
        fontSizeGrowth: 0.8            // minFontSize + fontSizeGrowth * keyword.score (df)   
    },
    // NEIGHBORS CLOUD
    neighborscloud: {
        minFontSize : 10,               // in px    
        fontSizeGrowth: 0.8               // minFontSize + fontSizeGrowth * keyword.score (df)   
    },
    // TAG BOX (droppable area)
    tagBox: {
        header: {
            enabled: false,
            useHybrid: false,
            useSplit: false
        },
        // useHybridHeader : false,
        aes: {
            defaultBlockStyle: false
        }
    },
    // DOCUMENT LIST
    contentList: {
        aes: {
            textDecoration: 'word'
        },
        header: false,                   // boolean
        custom: false,
        customOptions: {                //  only used when contentListType.custom = true
            selectors: {
                root: '',
                ul: '',
                liClass: '',
                liTitle: '',
                liRankingContainer: '',  // will be formatted
                watchicon: '',           // adds watchicon in placeholder
                favicon: ''              // adds favicon in placeholder
            },
            classes: {
                liHoverClass: '',
                liLightBackgroundClass: '',
                liDarkBackgroundClass: ''
            },
            misc: {
                hideScrollbar: true
            }
        },
    },
    // VISCANVAS --> RANKING VIEW
    visCanvas : {
        view: 'ranking',
        ranking: {},
        aes: {
            lightBackgroundColor: '',
            darkBackgroundColor: '',
            hideScrollbar: false
        }
    },
    // DOCUMENT VIEWER
    docViewer: {
        attrToShow: [],
        aes: {
            defaultBlockStyle: true,
            customScrollBars: true,
            textDecoration: 'background'
        }
    },
    // COLOR SCALES
    colors : {
        keyword: ['#eff3ff','#c6dbef','#9ecae1','#6baed6','#4292c6'], //colorbrewer.Greys[7].slice(2, 7)
        query: colorbrewer.Set1[9], //.splice(colorbrewer.Set1[9].indexOf("#ffff33"), 1, "#ffd700"), 
        usertag: ['#4daf4a'], //  ['#ffa32f']
        neighbor: ['#4daf4a']
    },
    // FETCH DATA 
    dataConnector : {
        urls :{
            get_data: null,             // GET
            get_keywords: null,         // GET
            get_tags: null,             // GET
            get_usertags: null,         // GET
            get_neighbors: null,        // GET
            urank: null,                // POST if this one is used, the following 3 are ignored
            update_ranking: null,       // POST
            clear_ranking: null,        // POST
            show_more_ranking: null,    // POST
            get_document_details: null  // POST
        }
    },
    // CALLBACKS
    callbacks : {
        onLoad: function(keywords){},
        onUpdate: function(selectedKeywords){},
        afterChange: function(rankingData, selectedKeywords){},
        onItemClicked: function(document){},        //done
        onItemMouseEnter: function(document){},
        onItemMouseLeave: function(document){},
        onFaviconClicked: function(document){},
        onWatchiconClicked: function(document){},
        onTagSelected: function(tag){},
        onTagInCloudMouseEnter: function(tag){},
        onTagInCloudMouseLeave: function(tag){},
        onTagInCloudClick: function(tag){},
        onTagDropped: function(droppedTags, dropMode){},
        onTagDeleted: function(tag){},
        onTagWeightChanged: function(tag){},
        onTagInBoxMouseEnter: function(index){},
        onTagInBoxMouseLeave: function(index){},
        onTagInBoxClick: function(index){},
        onTagFrequencyChanged: function(min, max){},
        onKeywordEntered: function(term){},
        onDocViewerHidden: function(){},
        onReset: function(){},
        onRankingWeightChanged: function(rsWeight){},
        onRatingClicked: function(documentId, index, rating){}
    }    
};

module.exports = Config;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(23)))

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(_, $, d3) {// var $ = require('jquery');
var VIEWS = __webpack_require__(4);
var Config = __webpack_require__(6);
var DataConnector = __webpack_require__(11);
var KeywordExtractor = __webpack_require__(12);
var RankingModel = __webpack_require__(13);
var ContentList = __webpack_require__(14);
var DocViewer = __webpack_require__(15);
var TagBox = __webpack_require__(17);
var TagCloud = __webpack_require__(18);
var UsertagBox = __webpack_require__(20);
var VisCanvas = __webpack_require__(21);
var NeighborsCloud = __webpack_require__(16);



var Urank = (function() {
    var _this, config, views, colorScales, callbacks, rankingConf, attr;
    var dataConn, rankingModel, selectedId, data, rankingData, keywordExtractor, tags;
    
    ////////////////////////////////////////////////////////////////////////////////////////
    //  METHODS PASSED TO VIEWS AND CALLED UPON EVENT OCCURRENCES
    ////////////////////////////////////////////////////////////////////////////////////////
    var EVTHANDLER = {
        // TAGCLOUD
        onTagSelected: function(index, id, is_multiple) {
            var stem = _this.keywords[index].stem;
            var term = _this.keywords[index].term;
            var tag_color =  getSelectedTagColor(stem, 'keyword');
            var tag = { type: 'keyword', id: id, index: index, stem: stem, color: tag_color, weight: 1, name: term };
            // { type: 'keyword', id: id, index: index, color: color, weight: 1 };
            views.tagBox.appendTag(tag);
            views.tagCloud.updateClonOfDroppedTag(index, id, tag_color);
            _this.selectedFeatures.keywords.push(tag);
            
            // if(!is_multiple) {
            URANK.update(_this.selectedFeatures);
            callbacks.onTagSelected.call(this, tag);
            // }
        },
        onMultipleTagsSelected: function(tags_arr) {
            // var droppedTags = []
            tags_arr.forEach(function(tag) {
                EVTHANDLER.onTagSelected(tag.index, tag.id, true);
                // droppedTags.push(tag);
            });
            // Add CALLBACK
        },

        onKeywordEntered: function(keyword){
            views.tagCloud.focusTag(keyword);
            callbacks.onKeywordEntered.call(this, keyword);
        },

        onTagFrequencyChanged: function(min, max){
            views.tagCloud.showTagsWithinRange(min, max)
            callbacks.onTagFrequencyChanged.call(this, min, max);
        },

        onTagInCloudClick: function(index, id) {
            // FIX HERE --> request bearing documents to server
            var idsArray = _this.keywords[index].inDocument;
            views.contentList.highlightListItems(idsArray);
            views.visCanvas.highlightItems(idsArray).resize(views.contentList.getListHeight());
            var tag = { index: index, id: id, term: _this.keywords[index].term }
            callbacks.onTagInCloudClick.call(this, tag);
        },

        // TAG BOX
        onTagDeleted: function(tag) {
            
            var featureType = tag.type + 's'
            var indexToDelete = _.findIndex(_this.selectedFeatures[featureType], function(t){
                return t.id.toString() === tag.id.toString();
            });
            // _this.selectedKeywords.splice(indexToDelete, 1);
            _this.selectedFeatures[featureType].splice(indexToDelete, 1);
            if(featureType === 'keywords') {
                views.tagCloud.restoreTag(tag.index, tag.id);
            } else if (featureType === 'neighbors') {
                views.neighborsCloud.restoreTag(tag.index, tag.id)
            }
            views.tagBox.deleteTag(tag);
            URANK.update(_this.selectedFeatures);
            callbacks.onTagDeleted.call(this, tag);
        },

        onTagWeightChanged: function(tag /*index, id, weight*/){
            var featureType = tag.type + 's'
            var indexToUpdate = _.findIndex(_this.selectedFeatures[featureType], function(t){
                return t.id.toString() === tag.id.toString();
            });
            _this.selectedFeatures[featureType][indexToUpdate].weight = tag.weight;            
            URANK.update(_this.selectedFeatures);            
            callbacks.onTagWeightChanged.call(this, tag);
        },

        onTagInCloudMouseEnter: function(index, id) {
            views.tagCloud.hoverTag(index, id);
            // var tag = { index: index, id: id, term: _this.keywords[index].term }
            // callbacks.onTagInCloudMouseEnter.call(this, tag);
        },

        onTagInCloudMouseLeave: function(index, id) {
            views.tagCloud.unhoverTag(index, id);
            // var tag = { index: index, id: id, term: _this.keywords[index].term }
            // callbacks.onTagInCloudMouseLeave.call(this, tag);
        },

        // USERTAGS
        onUsertagSelected: function(index, id) {
            var color =  getSelectedTagColor(_this.usertags[index].tag, 'usertag');
            var usertag = { type: 'usertag', id: id, index: index, color: color, weight: 1 };
            // _this.selectedUsertags.push(usertag);
            _this.selectedFeatures.usertags.push(usertag);
            views.usertagBox.selectUsertag(index, id, color);
            views.tagBox.appendTag(usertag);
        },
        onUsertagMouseEnter: function(index, id) {
            views.usertagBox.onUsertagMouseEnter(index, id);
        },

        onUsertagMouseLeave: function(index, id) {
            views.usertagBox.onUsertagMouseLeave(index, id);
        },

        // NEIGHBOR TAGS
        onNeighborTagSelected: function(index, id) {
            var tag_name = _this.neighbors[index].neighbor.name;
            var tag_color =  getSelectedTagColor(tag_name, 'neighbor');
            var neighbortag = { type: 'neighbor', id: id, index: index, name: tag_name, color: tag_color, weight: 1 };
            // _this.selectedNeighbors.push(neighbortag);
            _this.selectedFeatures.neighbors.push(neighbortag);
            views.neighborsCloud.selectNeighborTag(index, id, tag_color);
            views.tagBox.appendTag(neighbortag);
            URANK.update(_this.selectedFeatures);
            callbacks.onTagSelected.call(this, neighbortag);
        },
        onNeighborTagMouseEnter: function(index, id) {
            views.neighborsCloud.onNeighborTagMouseEnter(index, id);
        },

        onNeighborTagMouseLeave: function(index, id) {
            views.neighborsCloud.onNeighborTagMouseLeave(index, id);
        },

        // TAGCLOUD
        onTagInBoxMouseEnter: function(index) {
            // TODO
            callbacks.onTagInBoxMouseEnter.call(this, index);
        },

        onTagInBoxMouseLeave: function(index) {
            // TODO
            callbacks.onTagInBoxMouseLeave.call(this, index);
        },

        onTagInBoxClick: function(index) {
            callbacks.onTagInBoxClick.call(this, index);
        },
        // RANKING VIEW OR CONTENT LIST
        onItemClicked : function(documentId, index) {
            URANK.showDocument(documentId, index);
        },

        onItemMouseEnter: function(documentId, index) {
            views.contentList.hover(documentId, index);
            views.visCanvas.hoverItem(documentId, index);
            callbacks.onItemMouseEnter.call(this, { index: index, id: documentId, title: data[index][attr.title] });
        },

        onItemMouseLeave: function(documentId, index) {
            views.contentList.unhover(documentId, index);
            views.visCanvas.unhoverItem(documentId, index);
            callbacks.onItemMouseLeave.call(this, { index: index, id: documentId, title: data[index][attr.title] });
        },

        onFaviconClicked: function(documentId, index, state){
            views.contentList.toggleFavicon(documentId, index, state);
            callbacks.onFaviconClicked.call(this, { index: index, id: documentId, title: data[index][attr.title], state: state });
        },

        onWatchiconClicked: function(documentId, index) {
            views.contentList.toggleWatchListItem(documentId, index);
            callbacks.onWatchiconClicked.call(this, { index: index, id: documentId, title: data[index][attr.title] });
        },

        onDocViewerHidden: function() {
            views.docViewer.clear();
            views.contentList.deselectAllListItems();
            views.visCanvas.deselectAllItems();
        },

        onRootMouseDown: function(event){
            event.stopPropagation();
            if(event.which == 1) {
                views.tagCloud.clearEffects();
            }
        },

        onRootClick: function(event) {
            if(event.which == 1) {
                views.contentList.clearEffects();
                views.visCanvas.clearEffects().resize(views.contentList.getListHeight());
                views.docViewer.clear();
            }
        },

        onParallelBlockScrolled: function(sender, offset) {
            if(sender === views.contentList)
                views.visCanvas.scrollTo(offset);
            else if(sender == views.visCanvas)
                views.contentList.scrollTo(offset);
        },

        onResize: function(event) {
            views.visCanvas.resize();
        },

        onKeyDown: function(event){
            if(event.keyCode === 27)
                EVTHANDLER.onDocViewerHidden();
        },

        onRankingModeChange: function(mode) {
            console.log('rank by = ' + mode);
            setTimeout(function(){
                if(rankingConf.rank_by !== mode) {
                    rankingConf.rankBy = mode;
                    views.tagBox.updateRankingMode(mode);
                    // if(_this.selectedKeywords.length > 0)
                    URANK.update(_this.selectedFeatures);
                }
            }, 0);
        },

        onRankingWeightChange: function(rWeight) {
            var indexMapping = {}
            rankingConf.rs.forEach(function(conf){
                if(conf.name === 'CB') {
                    conf.weight = 1.0 - parseFloat(rWeight)
                } else {
                    conf.weight = parseFloat(rWeight)
                }
            })
            setTimeout(function() {
                // rankingConf.rs.CB = parseFloat(rWeight);
                // rankingConf.rs.CF = parseFloat(1-rWeight);
                URANK.update(_this.selectedFeatures);
                callbacks.onRankingWeightChanged.call(this, rWeight);
            }, 0);
        },

        onReset: function(event) {
            if(event) event.stopPropagation();
            URANK.reset();
        },

        onRatingClicked: function(documentId, index, rating){
            callbacks.onRatingClicked.call(this, documentId, index, rating);
        }
    };

    ////////////////////////////////////////////////////////////////////////////////
    // URANK  FUNCTIONS
    ////////////////////////////////////////////////////////////////////////////////
    var URANK = {
        
        // Initialize views
        initViews:  function(_config){
            var viewsConf = {
                contentList: {
                    root: _config.elem.contentListRoot,    
                    attr : _config.dataAttr,
                    options : _config.contentList,
                    cb : {
                        onItemClicked: EVTHANDLER.onItemClicked,
                        onItemMouseEnter: EVTHANDLER.onItemMouseEnter,
                        onItemMouseLeave: EVTHANDLER.onItemMouseLeave,
                        onFaviconClicked: EVTHANDLER.onFaviconClicked,
                        onWatchiconClicked: EVTHANDLER.onWatchiconClicked,
                        onScroll: EVTHANDLER.onParallelBlockScrolled,
                        onRatingClicked: EVTHANDLER.onRatingClicked
                    }
                },

                tagCloud: {
                    root: _config.elem.tagCloudRoot,
                    // view: _config.tagCloud.view,  //VIEWS.TAGCLOUD[_config.tagCloud.module],
                    attr : _config.dataAttr,
                    options : $.extend(true, _config.tagCloud, _config.rankingRepresentation),
                    cb : {
                        onKeywordEntered: EVTHANDLER.onKeywordEntered,
                        onTagFrequencyChanged: EVTHANDLER.onTagFrequencyChanged,
                        onTagInCloudMouseEnter: EVTHANDLER.onTagInCloudMouseEnter,
                        onTagInCloudMouseLeave: EVTHANDLER.onTagInCloudMouseLeave,
                        // details-on-demand click
                        onTagInCloudClick: EVTHANDLER.onTagInCloudClick,
                        // click to update ranking
                        onTagSelected: EVTHANDLER.onTagSelected
                    }
                },

                tagBox: {
                    root: _config.elem.tagBoxRoot,
                    // options: $.extend(true, {
                    //     useHybridHeader : _config.rankingModel.rs.CB.active && _config.rankingModel.rs.TU.active
                    // }, _config.tagBox, _config.rankingRepresentation),
                    options: _config.tagBox,
                    cb : {
                        onModeChanged: EVTHANDLER.onRankingModeChange,
                        onRankingWeightChanged: EVTHANDLER.onRankingWeightChange,
                        onTagSelected: EVTHANDLER.onTagSelected,       // triggered on atg dropped
                        onMultipleTagsSelected: EVTHANDLER.onMultipleTagsSelected,
                        onTagDeleted: EVTHANDLER.onTagDeleted,
                        onTagWeightChanged: EVTHANDLER.onTagWeightChanged,
                        onTagInBoxMouseEnter: EVTHANDLER.onTagInBoxMouseEnter,
                        onTagInBoxMouseLeave: EVTHANDLER.onTagInBoxMouseLeave,
                        onTagInBoxClick: EVTHANDLER.onTagInBoxClick,
                        onReset: EVTHANDLER.onReset
                    }
                },

                visCanvas: {
                    root: _config.elem.visCanvasRoot,
                    // view : _config.visCanvas.view, //VIEWS.VISCANVAS[_config.visCanvas.module],
                    attr : _config.dataAttr,
                    options : $.extend(true, _config.visCanvas, _config.rankingRepresentation),
                    cb : {
                        onItemClicked: EVTHANDLER.onItemClicked,
                        onItemMouseEnter: EVTHANDLER.onItemMouseEnter,
                        onItemMouseLeave: EVTHANDLER.onItemMouseLeave,
                        onScroll: EVTHANDLER.onParallelBlockScrolled
                    }
                },

                docViewer: {
                    root: _config.elem.docViewerRoot,
                    attr : _config.dataAttr,
                    options : _config.docViewer,
                    cb :{
                        onDocViewerHidden: EVTHANDLER.onDocViewerHidden    
                    }
                },

                usertagBox : {
                    root: _config.elem.usertagBox,
                    attr: _config.attr,
                    options: _config.usertagBox,
                    cb : {
                        onUsertagMouseEnter: EVTHANDLER.onUsertagMouseEnter,
                        onUsertagMouseLeave: EVTHANDLER.onUsertagMouseLeave,
                        onUsertagSelected: EVTHANDLER.onUsertagSelected
                    }
                },

                neighborsCloud : {
                    root: _config.elem.neighborscloudRoot,
                    attr: _config.attr,
                    options: _config.neighborscloud,
                    cb : {
                        onNeighborTagMouseEnter: EVTHANDLER.onNeighborTagMouseEnter,
                        onNeighborTagMouseLeave: EVTHANDLER.onNeighborTagMouseLeave,
                        onNeighborTagSelected: EVTHANDLER.onNeighborTagSelected
                    }
                }
            };

            views = {
                contentList : new ContentList(viewsConf.contentList),
                tagCloud    : new TagCloud(viewsConf.tagCloud),
                tagBox      : new TagBox(viewsConf.tagBox),
                visCanvas   : new VisCanvas(viewsConf.visCanvas),
                docViewer   : new DocViewer(viewsConf.docViewer),
                usertagBox  : new UsertagBox(viewsConf.usertagBox),
                neighborsCloud: new NeighborsCloud(viewsConf.neighborsCloud)
            }

            //  Bind event handlers to resize window and undo effects on random clicks
            $(window).off('resize', EVTHANDLER.onResize).resize(EVTHANDLER.onResize);
            $(document).off('keydown', EVTHANDLER.onKeyDown).on('keydown', EVTHANDLER.onKeyDown);
            $(_config.elem.root).off({
                'mousedown': EVTHANDLER.onRootMouseDown,
                'click': EVTHANDLER.onRootClick
            }).on({
                'mousedown': EVTHANDLER.onRootMouseDown,
                'click': EVTHANDLER.onRootClick
            });
        },

        loadData: function(_data){
            data = _data.slice();
            // EVTHANDLER.loadData(_data);
            console.log('Loaded data = ' + _data.length)
            console.log(data[0])
            //Start ranking model (REPLACE)     
            rankingModel.clear().setData(data);    
            //Build views with data and/or keywords
            views.contentList.build(data, views.tagBox.getHeight());
            views.visCanvas.build(data, views.contentList.getListHeight());
        },

        // Load keywords in tag cloud
        loadKeywords: function(_keywords) {
            _this.keywords = _keywords;
            views.tagCloud.build(_this.keywords, data, colorScales.keyword);
        },

        // Load keywords synchronously with clint-side keyword extractor
        loadKeywordsSync: function(){
            var keywordExtractor = new KeywordExtractor(confKeywordExt);
            //  Clean documents and add them to the keyword extractor
            data.forEach(function(d, i){
                d.index = i;
                d[attr.title] = d[attr.title].clean();
                // var attr_desc = !attr.description_clean.isEmpty() ? attr.description_clean : attr.description;
                // d[attr_desc] = d[attr.description].clean();
                // var text = (d[attr_desc]) ? d[attr.title] +'. '+ d[attr_desc] : d[attr.title];
                var text = d[attr.title];
                keywordExtractor.addDocument(text.removeUnnecessaryChars(), d[attr.id]);
            });

            //  Extract collection and document keywords
            keywordExtractor.processCollection();

            // var kwExt = cleanAndExtractKeywords(data, config.keywordExtractor);
            //  Assign document keywords
            data.forEach(function(d, i){
                d.keywords = keywordExtractor.listDocumentKeywords(i);
            });
            //  Assign collection keywords and set other necessary variables
            _keywords = keywordExtractor.getCollectionKeywords();
            this.loadKeywords(_keywords);
        },

        // Load document tags (unused)
        loadTags: function(_tags){
        },

        // Load user tags (from user model)
        loadUserTags: function(_usertags) {
            _this.usertags = _usertags;
            views.usertagBox.build(_this.usertags, colorScales.usertag);
        },

        loadNeighbors: function(_neighbors) {
            // TODO
            _this.neighbors = _neighbors
            console.log(_this.neighbors[0])
            views.neighborsCloud.build(_this.neighbors, colorScales.neighbor)
        },

        // Update ranking
        update: function(_selectedFeatures) {
            // _this.selectedKeywords = _selectedKeywords || _this.selectedKeywords;
            _this.selectedFeatures = _selectedFeatures
            selectedId = undefined;
            console.log(rankingConf);

            var emptyFeat = true;
            for(var feature in _this.selectedFeatures) {
                if(_this.selectedFeatures[feature].length){
                    emptyFeat = false;
                }
            }
            if(emptyFeat) {
                return URANK.reset();
            }
            // Update ranking config
            var params = {
                rs_conf: rankingConf,
                features: _this.selectedFeatures,
                decoration: config.contentList.aes.textDecoration
            };

            rankingModel.update(params, function(_ranking, _status){
                rankingData = _ranking;
                status = _status;
                // Update views
                views.contentList.update({ 
                    ranking: rankingData.slice(),
                    status: status
                });
                views.visCanvas.update({
                    status: status,
                    ranking: rankingData,
                    conf: rankingConf,
                    // query: _this.selectedKeywords,
                    features: _this.selectedFeatures,
                    // query: _this.selectedFeatures.keywords,
                    colorScale: colorScales.query,
                    listHeight: views.contentList.getListHeight()
                });
                views.docViewer.clear();
                views.tagCloud.clearEffects();
                // Callback specified by main.js
                // callbacks.onUpdate.call(this, rankingData, _this.selectedKeywords, status);
            });
        },

        // Show clicked document
        showDocument: function(documentId, index) {
            selectedId = documentId;
            views.contentList.selectListItem(documentId, index);
            views.visCanvas.selectItem(documentId, index);
            views.tagCloud.clearEffects();
            // Fetch pretty title and abstract
            var params = {
                doc_id: documentId, 
                doc_index: index, 
                decoration: config.docViewer.aes.textDecoration
            };
            // console.log('index = '+index);
            // console.log('id = ' + documentId);
            dataConn.getDocumentDetails(params, function(doc) {
                views.docViewer.showDocument(doc);
                callbacks.onItemClicked.call(this, { index: index, id: documentId, title: data[index][attr.title] });
            });
        },
            
        // Reset
        reset: function(){
            views.contentList.reset();
            views.tagBox.reset();
            //tagCloud.reset();
            views.visCanvas.reset();
            views.docViewer.clear();
            for(var feature in _this.selectedFeatures){
                _this.selectedFeatures[feature].forEach(function(tag, i){
                    setTimeout(function(){
                        if(feature === 'keywords') {
                            views.tagCloud.restoreTag(tag.index, tag.id);    
                        } else if(feature === 'neighbors') {
                            views.neighborsCloud.restoreTag(tag.index, tag.id)
                        } else if (feature === 'usertags') {
                            views.usertagBox.restoreTag(tag.index, tag.id);
                        }
                        views.tagBox.deleteTag(tag);
                        
                    }, (i+1)*50);
                });    
            }
            
            // _this.selectedKeywords = [];
            _this.selectedFeatures.keywords = [];
            callbacks.onReset.call(this);
        }

    }



    ////////////////////////////////////////////////////////////////////////////////
    // INTERNAL FUNCTIONS
    ////////////////////////////////////////////////////////////////////////////////

    var getOrdinalColorScale = function(colors, numCategories) {
        numCategories = numCategories || colors.length;
        if(colors.length > numCategories) {
            colors = colors.slice(colors.length-numCategories, colors.length);
        }
        // if numCategories > 0, preset domain, otherwise it's updated on-demand (e.g. query terms)
        if(numCategories)
            return d3.scale.ordinal().domain(d3.range(0, numCategories, 1)).range(colors);  
        return d3.scale.ordinal().range(colors);
    };


    var getSelectedTagColor = function(name, type){
        var color;
        if(config.rankingRepresentation.split_by === 'rs') {
            if(type === 'keyword') {
                color = colorScales.keyword(name);
            } else if(type === 'usertag') {
                color = colorScales.usertag(name);
            } else if(type === 'neighbor') {
                color = colorScales.neighbor(name);
            }
        } else if(config.rankingRepresentation.split_by === 'feature') {
            color = colorScales.query(name);
        }
        return color;
    }


    ////////////////////////////////////////////////////////////////////////////////////////
    // CONSTRUCTOR
    ////////////////////////////////////////////////////////////////////////////////////////
    function Urank(options) {
        _this = this;
        data = [];
        this.keywords = [];
        this.usertags = [];
        this.neighbors = [];
        this.selectedKeywords = [];
        this.selectedUsertags = [];
        this.selectedNeighbors = [];
        this.selectedFeatures = {}; // keywords, neighbors, usertags, ...
        selectedId = undefined;

        // Extend config.js with custom options
        config = $.extend(true, Config, options || {});
        dataConn = new DataConnector(config.dataConnector);
        rankingModel = new RankingModel(config.rankingModel, dataConn);
        Object.keys(config.features).forEach(function(feature){
            _this.selectedFeatures[feature] = [];
        });
    
        attr = config.dataAttr;
        callbacks = config.callbacks;
        colorScales = {
            keyword : getOrdinalColorScale(config.colors.keyword, config.tagCloud.numCategories),
            usertag: getOrdinalColorScale(config.colors.usertag),
            neighbor: getOrdinalColorScale(config.colors.neighbor),
            query : getOrdinalColorScale(config.colors.query, 0)
        };
        rankingConf = config.rankingModel;
        console.log(rankingConf);
        URANK.initViews(config);
    }

    ////////////////////////////////////////////////////////////////////////////////////////
    // PROTOTYPE METHODS
    ////////////////////////////////////////////////////////////////////////////////////////

    var load = function(_data) {
        views.tagBox.build(rankingConf);
        views.docViewer.build();
        // LOAD DOCUMENTS
        if(_data) {
            URANK.loadData(_data)
        } else {
            dataConn.getData(URANK.loadData);
        }
        // LOAD KEYWORDS
        if(config.features.keywords) {
            // ASYNC load if local keyword extractor is disabled
            if(config.keywordExtractor.useLocal) {
                URANK.loadKeywordsSync();    
            } else {
                dataConn.getKeywords(URANK.loadKeywords);
            }
        }
        // LOAD TAGS (nothing happens if config.data_connector.urls.get_tags = null)
        dataConn.getTags(URANK.loadTags);
        // LOAD USERTAGS (nothing happens if config.data_connector.urls.get_usertags = null)
        if(config.features.usertags)
            dataConn.getUsertags(URANK.loadUserTags);
        // LOAD NEIGHBORS
        if(config.features.neighbors)
            dataConn.getNeighbors(URANK.loadNeighbors);
        //  Custom callback
        callbacks.onLoad.call(this);
    };


    var destroy = function() {
        views.tagCloud.destroy();
        views.tagBox.destroy();
        views.contentList.destroy();
        views.visCanvas.destroy();
        views.docViewer.destroy();
    };

    var clear = function() {
        views.tagCloud.clear();
        views.tagBox.clear();
        views.docViewer.clear();
//            contentList.clear();
        //visCanvas.destroy();
    };

    var bookmarkItem = function(documentId, index){
        data[index].bookmarked = true;
        views.contentList.toggleFavicon(documentId);
    };

    var unbookmarkItem = function(documentId, index){
        data[index].bookmarked = false;
        views.contentList.toggleFavicon(documentId);
    };

    //  Miscelaneous
    var getCurrentState = function(){
        return {
            mode: rMode,
            status: rankingModel.getStatus(),
            selectedKeywords: _this.selectedKeywords.map(function(sk){ return { term: sk.term, weight: sk.weight } }),
            ranking: rankingModel.getRanking().map(function(d){
                return {
                    id: d[attr.id],
                    title: d[attr.title],
                    rankingPos: d.rankingPos,
                    overallScore: d.overallScore,
                    maxScore: d.maxScore,
                    positionsChanged: d.positionsChanged,
                    weightedKeywords: d.weightedKeywords.map(function(wk){ return { term: wk.term, weightedScore: wk.weightedScore } })
                }
            })
        };
    };

    var getSelectedKeywords = function(){ 
        return _this.selectedKeywords 
    };

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype
    ////////////////////////////////////////////////////////////////////////////////////////////////////
    Urank.prototype = {
        load: load,
        clear: clear,
        destroy: destroy,
        bookmarkItem: bookmarkItem,
        unbookmarkItem: unbookmarkItem,
        getCurrentState: getCurrentState,
        getSelectedKeywords: getSelectedKeywords
    };

    return Urank;
})();

module.exports = Urank;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(1), __webpack_require__(0), __webpack_require__(2)))

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(jQuery) {
(function($) {

    $.fn.extend({
        pin: function(args) {

            var options = $.extend({
                top: 0,
                left: 0,
                bottom: 0,                  // only if relativeTo != 'none'
                right: 0,                   // only if relativeTo != 'none'
                container: 'window',
                relativeTo: 'parent'        // parent | none | custom selector
            }, args);

            return this.each(function() {
                var $this = $(this);
                if($this.css('visibility') == 'visible') {

                    if(options.relativeTo !== 'none') {
                        var $parent = options.relativeTo == 'parent' ? $this.parent() : options.relativeTo;
                        options.left = options.right ? options.left + $parent.fullOffset().left + $parent.fullWidth() + options.right : options.left + $parent.fullOffset().left;
                        options.top = options.bottom ? options.top + $parent.fullOffset().top + $parent.fullHeight() + options.bottom : options.top + $parent.fullOffset().top;
                    }

                    $this.css({ position: 'fixed', top: options.top, left: options.left, 'z-index': 9999 });

                    if(options.container !== 'window') {
                        var $container = $(options.container),
                            containerOffset = $container.offset(),
                            containerHeight = $container.height(),
                            //     containerWidth = $container.width(),
                            thisOffset = $this.fullOffset(),
                            thisHeight = $this.height();
                        //   thisWidth = $this.width();

                        if(thisOffset.top < containerOffset.top || (thisOffset.top + thisHeight) > (containerOffset.top + containerHeight)
                           /*|| thisOffset.left < containerOffset.left || (thisOffset.left + thisWidth) > containerOffset.left + containerWidth */)
                            $this.css('visibility', 'hidden');
                    }
                }
                return $this;
            });
        },
        
        fullHeight: function() {
            var m = {
                border: {
                    top: $(this).css('border-top-width') || '0px',
                    bottom: $(this).css('border-bottom-width') || '0px'
                },
                padding: {
                    top: $(this).css('padding-top') || '0px',
                    bottom: $(this).css('padding-bottom') || '0px'
                }
            };

            return $(this).height()
                + parseInt(m.border.top.replace('px', ''))
                + parseInt(m.padding.top.replace('px', ''))
                + parseInt(m.border.bottom.replace('px', ''))
                + parseInt(m.padding.bottom.replace('px', ''));
        },

        fullOffset: function() {
            return {
                top: $(this).offset().top + parseInt($(this).css('margin-top').replace('px', '')),
                    //  parseInt($(this).css('border-top-width').replace('px', '')) +
                    //parseInt($(this).css('padding-top').replace('px', '')) +
                left: $(this).offset().left + parseInt($(this).css('margin-left').replace('px', ''))
                    //parseInt($(this).css('border-left-width').replace('px', '')) +
                    //parseInt($(this).css('padding-left').replace('px', ''))
            };
        },

        fullWidth: function() {
            return $(this).width()
                + parseInt($(this).css('border-left-width').replace('px', ''))
                + parseInt($(this).css('padding-left').replace('px', ''))
                + parseInt($(this).css('border-right-width').replace('px', ''))
                + parseInt($(this).css('padding-right').replace('px', ''));
        },

        getText: function() {
            return $(this).clone().children().remove().end().text();
        },

        outerHTML: function() {
            return $(this).clone().wrap('<div></div>').parent().html();
        },

        scrollTo: function(target, options, callback){

            if(typeof options == 'function' && arguments.length == 2){
                callback = options;
                options = target;
            }

            var settings =
                $.extend({
                    scrollTarget  : target,
                    offsetTop     : 0,
                    duration      : 500,
                    easing        : 'swing'
                }, options);

            return this.each(function(){
                var scrollPane = $(this);

                var scrollTarget;
                if( typeof settings.scrollTarget == "number" ){
                    scrollTarget = settings.scrollTarget;
                }
                else{
                    if( settings.scrollTarget == "top" ){
                        scrollTarget = 0;
                    }
                    else{
                        scrollTarget = $(settings.scrollTarget);
                        settings.offsetTop += scrollPane.offset().top;
                    }
                }

                //var scrollTarget = (typeof settings.scrollTarget == "number") ? settings.scrollTarget : $(settings.scrollTarget);
                var scrollY = (typeof scrollTarget == "number") ? scrollTarget : scrollPane.scrollTop() + scrollTarget.offset().top - settings.offsetTop;

                scrollPane.animate({scrollTop : scrollY }, parseInt(settings.duration), settings.easing, function(){
                    if (typeof callback == 'function') { callback.call(this); }
                });
            });
        },

        // unfinished
        tooltip: function(options) {

            var tooltipClass = 'urank-tooltip';

            var $this = $(this);


            if(typeof options == 'string' && options == 'destroy'){


            } else if(typeof options == 'object') {
                var s = $.extend({
                    title: null,
                    message: '',
                    position: 'right',      //  right | left | top | bottom
                    type: 'default',        //  default | info |
                    root: 'body'
                }, options);

                $tooltip = $('<div></div>', { class: tooltipClass }).appendTo($this);

            }

            return $this;
        }

    });
    
    
}(jQuery));

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(d3) { 

module.exports = {
    /**
     * parsing functions
     *
     * */
    parseDate: function( dateString ){
        if(dateString instanceof Date)
            return dateString;

        var yearFormat = d3.time.format("%Y");
        var date = yearFormat.parse(dateString);

        if(date != null) return date;

        var dateFormat = d3.time.format("%Y-%m");
        date = dateFormat.parse(dateString);

        if(date != null) return date;

        if( dateString.length == 8 )
            date = yearFormat.parse( dateString.substring(0, 4) );

        if(date != null) return date;

        if(dateString.contains("c "))
            date = yearFormat.parse( dateString.substring(2, 6) );

        if(date != null) return date;
        return yearFormat.parse('2014');
    },

    toYear: function(date){
        var formatYear = d3.time.format("%Y");
        var year = formatYear(date);    
            return year;
    },

    getTimestamp: function() {
        var date = new Date(),
            year = date.getFullYear(),
            month = (date.getMonth()+1) < 10 ? '0'+(date.getMonth()+1) : (date.getMonth()+1),
            day = date.getDay() < 10 ? '0'+date.getDay() : date.getDay(),
            hour = date.getHours(),
            min = date.getMinutes(),
            mil = date.getMilliseconds();
        return year+'-'+month+'-'+day+'_'+hour+'.'+min+'.'+mil;
    },

    /////////////////////////////////////////////////////////////////////////////////////////////////////
    /**
     * hex to RGB converter
     * */
    cutHex: function (h) {
        return (h.charAt(0) == "#") ? h.substring(1, 7) : h
    },
    hexToR: function (h) {
        return parseInt((this.cutHex(h)).substring(0, 2), 16)
    },
    hexToG: function (h) {
        return parseInt((this.cutHex(h)).substring(2, 4), 16)
    },
    hexToB: function (h) {
        return parseInt((this.cutHex(h)).substring(4, 6), 16)
    },
    /////////////////////////////////////////////////////////////////////////////////////////////////////
    /**
     * format gradient string
     * */
     getGradientString: function(color, shadeDiff) {

        shadeDiff = shadeDiff || 10;
        var r = parseInt(hexToR(color));
        var g = parseInt(hexToG(color));
        var b = parseInt(hexToB(color));

        var original = 'rgb('+r+','+g+','+b+')';
        var lighter = 'rgb('+(r+shadeDiff)+','+(g+shadeDiff)+','+(b+shadeDiff)+')';

        if (navigator.userAgent.search("MSIE") >= 0) {
            return '-ms-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
        }
        else if (navigator.userAgent.search("Chrome") >= 0) {
            return '-webkit-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
        }
        else if (navigator.userAgent.search("Firefox") >= 0) {
            return '-moz-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
        }
        else if (navigator.userAgent.search("Safari") >= 0 && navigator.userAgent.search("Chrome") < 0) {
            return '-webkit-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
        }
        else if (navigator.userAgent.search("Opera") >= 0) {
            return '-o-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
        }
        return '-webkit-linear-gradient(top, ' + original + ', ' + lighter + ', ' + original + ')';
    }


};



/////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * String prototype
 *
 * */

String.prototype.contains = function(it) {
    return this.indexOf(it) != -1;
};


String.prototype.toBool = function() {
    return (this == "true");
};

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

String.prototype.isAllUpperCase = function() {
    return this.valueOf().toUpperCase() === this.valueOf();
};

String.prototype.clean = function(){

    function decodeHTMLEntities (str) {
        var element = document.createElement('div');
        if(str && typeof str === 'string') {
            // strip script/html tags
            str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
            str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
            element.innerHTML = str;
            str = element.textContent;
            element.textContent = '';
        }
        return str;
    }

    var text = unescape(this.toString()),
        textArray = [],
        splitText = text.split(' ');

    for(var i = 0; i < splitText.length; ++i) {
        if(splitText[i].match(/\w+-$/)){
            textArray.push(splitText[i].replace('-', '') + splitText[i+1]);
            ++i;
        }
        else
            textArray.push(splitText[i]);
    }
    text = textArray.join(' ');
    return (text[text.length - 1] == ' ') ? text.substring(0, text.length-1) : text;
};


String.prototype.removeUnnecessaryChars = function() {
    return this.replace(/[-=’‘\']/g, ' ').replace(/[()\"“”]/g,'');
};

String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};


/////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Number prototype gunction to parse milliseconds to minutes:seconds format
 *
 * */

Number.prototype.toTime = function(){
    var min = (this/1000/60) << 0;
    var sec = Math.floor((this/1000) % 60);
    if (min.toString().length == 1) min = '0' + min.toString();
    if (sec.toString().length == 1) sec = '0' + sec.toString();
    return min + ':' + sec;
};


Number.prototype.round = function(places) {
    return +(Math.round(this + "e+" + places)  + "e-" + places);
}


/////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Math prototype
 *
 * */

if(!Math.roundTo)
    Math.roundTo = function(value, places) { return +(Math.round(value + "e+" + places)  + "e-" + places); }


if(!Math.log2)
    Math.log2 = function(value) { return (Math.log(value) / Math.log(2)); }






/////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 *  NLP 
 *  Move to different file
 * */

// // 
// var natural = require('natural');
// var stemmer = natural.PorterStemmer;
// var nounInflector = new natural.NounInflector();
// stemmer.attach();
// nounInflector.attach();


// function getStyledText (text, stemmedKeywords, colorScale){
//     var styledText = '',
//         word = '';
//     text.split('').forEach(function(c){
//         if(c.match(/\w/)){
//             word += c;
//         }
//         else if(c == '\n'){
//             styledText += '<br/>'
//         }
//         else {
//             if(word != '')
//                 word = getStyledWord(word,stemmedKeywords, colorScale);
//             styledText += word + c;
//             word = '';
//         }
//     });
//     if(word != '')
//         styledText += getStyledWord(word, stemmedKeywords, colorScale);
//     return styledText;
// }


// function getStyledWord (word, stemmedKeywords, colorScale){
//     var trickyWords = ['it', 'is', 'us', 'ar'],
//         word = word.replace(/our$/, 'or'),
//         wordStem = word.stem();
//     // First clause solves words like 'IT', second clause that the stem of the doc term (or the singularized term) matches the keyword stem
//     if(trickyWords.indexOf(wordStem) == -1 || word.isAllUpperCase()) {
//         if(stemmedKeywords.indexOf(wordStem) > -1 )
//             return "<strong style='color:" + colorScale(wordStem) + "'>" + word + "</strong>";
//         if(stemmedKeywords.indexOf(word.singularizeNoun().stem()) > -1 )
//             return "<strong style='color:" + colorScale(word.singularizeNoun().stem()) + "'>" + word + "</strong>";
//     }
//     return word;
// }
// function getPositionArray (text, stemmedKeywords, position){
//     var positionArray = [];

//     var word = '';
//     text.split('').forEach(function(c){
//         position++;
//         if(c.match(/\w/))
//             word += c;
//         else {
//             if(word != '') {
//                 var returnValue = getPositionOfWord(word, stemmedKeywords, position);
//                 if(returnValue != null) {
//                     positionArray.push(returnValue);
//                     position = returnValue.position;
//                 }
//                 word = '';
//             }
//         }
//     });

//     if(word != '') {
//         var returnValue = getPositionOfWord(word, stemmedKeywords, position);
//         if(returnValue != null) {
//             positionArray.push(returnValue);
//             position = returnValue.position;
//         }
//         word = '';
//     }
//     return positionArray;
// }

// function getPositionOfWord (word, stemmedKeywords, position){

//     var trickyWords = ['it', 'is', 'us', 'ar'],
//         word = word.replace(/our$/, 'or'),
//         wordStem = word.stem();

//     // First clause solves words like 'IT', second clause that the stem of the doc term (or the singularized term) matches the keyword stem
//     if(trickyWords.indexOf(wordStem) == -1 || word.isAllUpperCase()) {
//         var positionArrayEntry;
//         var index = stemmedKeywords.indexOf(wordStem);

//         if(index > -1) {
//             positionArrayEntry = new Object;
//             positionArrayEntry.word = word;
//             positionArrayEntry.position = position - word.length / 2;
//             positionArrayEntry.keyword = stemmedKeywords[index];
//             return positionArrayEntry;
//         }

//         index = stemmedKeywords.indexOf(word.singularizeNoun().stem());
//         if(index > -1) {
//             positionArrayEntry = new Object;
//             positionArrayEntry.word = word;
//             positionArrayEntry.position = position - word.length / 2;
//             positionArrayEntry.keyword = stemmedKeywords[index];
//             return positionArrayEntry;
//         }
//     }

//     return null;
// }



/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(2)))

/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {
var RSContent = (function(){
    'use strict';

    // function RSContent() {}

    var getEuclidenNorm = function(docKeywords) {
        var acumSquares = 0;
        Object.keys(docKeywords).forEach(function(k){
            acumSquares += docKeywords[k] * docKeywords[k];
        });
        return Math.sqrt(acumSquares);
    };


    return {
        getCBScores : function(options) {
            var opt = $.extend(true, {
                data: [],
                keywords: [],
                options: {
                    rWeight: 1
                }
            }, options);
            var _data = opt.data.slice();

            if(opt.keywords.length > 0) {
                _data.forEach(function(d, i) {
                    d.ranking.cb_score = 0;
                    d.ranking.cb_max_score = 0;
                    d.ranking.cb_details = [];
                    var docNorm = getEuclidenNorm(d.keywords);
                    var unitQueryVectorDot = parseFloat(1.00/Math.sqrt(opt.keywords.length));
                    var max = 0;
                    opt.keywords.forEach(function(q) {
                    // termScore = tf-idf(d, t) * unitQueryVector(t) * weight(query term) / |d|   ---    |d| = euclidenNormalization(d)
                        var termScore = (d.keywords[q.stem]) ? ((parseFloat(d.keywords[q.stem]) / docNorm) * unitQueryVectorDot * parseFloat(q.weight * opt.options.rWeight)).round(3) :  0;
                        // if item doesn't contain query term => maxScore and overallScore are not changed
                        d.ranking.cb_score += termScore;
                        d.ranking.cb_max_score = termScore > d.ranking.cb_max_score ? termScore : d.ranking.cb_max_score;
                        d.ranking.cb_details.push({ term: q.term, stem: q.stem, weightedScore: termScore });
                    });
                });
            }
            return _data;
        }
    }
})();

module.exports = RSContent;



/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {
DataConnector = (function(){
	var _this;

	function DataConnector(options){
		this.urls = options.urls;
		_this = this;
	}

	var sendRequest = function(options, onDone, onFail){
		var request_options = $.extend(true, {
			'url' : '',
			'type': 'GET'
		}, options);
		onDone = onDone || function(data){};
		onFail = onFail || function(){};
		if(!request_options.url || request_options.url === '') return { 'message': 'No URL set' };
		var timelapse = $.now()
		$.ajax(request_options)
		.fail(function(jqXHR, textStatus){
	        console.log('DataConnector ERROR ' + request_options.type + ' ' + request_options.url);
	        // console.log(jqXHR)
	        onFail();
	    }).done(function(resp) {
	        timelapse = $.now() - timelapse
	        console.log('DataConnector: successful request ' + request_options.type + ' ' + request_options.url + ' (' + timelapse + ' ms)');
        	console.log(resp.results.length);    
	        onDone(resp.results);
	    });

	};

	var getData = function(onDone) {
		sendRequest({ url: _this.urls.get_data }, onDone);
	};

	var getKeywords = function(onDone) {
		sendRequest({ url: _this.urls.get_keywords }, onDone);
	};

	var getTags = function(onDone){
		sendRequest({ url: _this.urls.get_tags }), onDone;
	};

	var getUsertags = function(onDone){
		sendRequest({ url: _this.urls.get_usertags }, onDone);
	};

	var getNeighbors = function(onDone){
		sendRequest({ url: _this.urls.get_neighbors }, onDone);
	};

	var postUrank = function(url, data, onDone){
		console.log('DataConnector: Start request --> ' + data.operation);
		sendRequest({ 
			'type': 'POST',
			'url': url, 
			'data':  JSON.stringify(data),
			'contentType': 'application/json; charset=utf-8'
		}, onDone);
	}

	var updateRanking = function(params, onDone) {
		var url = this.urls.urank || this.urls.update_ranking;
		var data = $.extend(true, { 'operation': 'update' }, params);
		postUrank(url, data, onDone);
	};

	var clearRanking = function(onDone) {
		var url = this.urls.urank || this.urls.clear_ranking;
		var data = { 'operation': 'clear' };
		postUrank(url, data, onDone);
	};

	var showMoreRanking = function(onDone){
		var url = this.urls.urank || this.urls.show_more_ranking;
		var data = { 'operation': 'show_more' };
		postUrank(url, done, onDone);
	};

	var getDocumentDetails = function(params, onDone){
		var url = this.urls.urank || this.urls.get_document_details;
		var data = $.extend(true, { 'operation': 'get_document_details' }, params);
		postUrank(url, data, onDone);
	};


	DataConnector.prototype = {
		getData: getData,
		getKeywords: getKeywords,
		getTags: getTags,
		getUsertags: getUsertags,
		getNeighbors: getNeighbors,
		updateRanking: updateRanking,
		clearRanking, clearRanking,
		showMoreRanking : showMoreRanking,
		getDocumentDetails: getDocumentDetails
	};

	return DataConnector;

})()


module.exports = DataConnector;
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($, _) {
var KeywordExtractor = (function(){

    var _this,
        s = {},
        stemmer, tokenizer, nounInflector, tfidf, stopWords, pos, lexer, tagger,
        POS = {
            NN: 'NN',           // singular noun
            NNS: 'NNS',         // plural noun
            NNP: 'NNP',         // proper noun
            JJ: 'JJ'            // adjective
        };

    //  CONSTRUCTOR
    function KeywordExtractor(options) {
        s = $.extend(true, {
            minDocFrequency: 2,
            minRepetitionsInDocument: 1,
            maxKeywordDistance: 5,
            minRepetitionsProxKeywords: 4
        }, options);
        _this = this;
        this.collection = [];
        this.documentKeywords = [];
        this.collectionKeywords = [];
        this.collectionKeywordsDict = {};

        stemmer = natural.PorterStemmer; //natural.LancasterStemmer;
        stemmer.attach();
        tokenizer = new natural.WordTokenizer;
        nounInflector = new natural.NounInflector();
        nounInflector.attach();
        //tfidf = new natural.TfIdf(),
        stopWords = natural.stopwords;
        pos = new Pos();
        lexer = new pos.Lexer();
        tagger = new pos.Tagger();
    }


/************************************************************************************************************************************
*
*   PRIVATE METHODS
*
************************************************************************************************************************************/



    var extractDocumentKeywords = function(collection) {

        //POS tagging
        collection.forEach(function(d, i) {
            d.taggedWords = tagger.tag(lexer.lex(d.text));
        });

        // Find out which adjectives are potentially important and worth keeping
        var keyAdjectives = getKeyAdjectives(collection);

        // Create each item's document to be processed by tf*idf
        collection.forEach(function(d) {
            d.tokens = getFilteredTokens(d.taggedWords, keyAdjectives);                                       // d.tokens contains raw nouns and important adjectives
            tfidf.addDocument(d.tokens.map(function(term){ return term.stem(); }).join(' '));                 // argument = string of stemmed terms in document array
        });

        // Save keywords for each document
        var documentKeywords = [];
        collection.forEach(function(d, i){
            documentKeywords.push(getDocumentKeywords(i));
        });

        return documentKeywords;
    };



    var getKeyAdjectives = function(_collection) {

        var candidateAdjectives = [],
            keyAdjectives = [];

        _collection.forEach(function(d, i) {
            // Find out which adjectives are potentially important and worth keeping
            d.taggedWords.forEach(function(tw){
                if(tw[1] == 'JJ'){
                    var adjIndex = _.findIndex(candidateAdjectives, function(ca){ return ca.adj === tw[0].toLowerCase() });
                    if(adjIndex == -1)
                        candidateAdjectives.push({ 'adj': tw[0].toLowerCase(), 'count': 1 });
                    else
                        candidateAdjectives[adjIndex].count++;
                }
            });
        });

        candidateAdjectives.forEach(function(ca){
            if(ca.count >= parseInt(_collection.length * 0.25))
                keyAdjectives.push(ca.adj);
        });
        return keyAdjectives;
    }


    // Filter out meaningless words, keeping only nouns (plurals are singularized) and key adjectives
    var getFilteredTokens = function(taggedWords, keyAdjectives) {
        var filteredTerms = [];
        taggedWords.forEach(function(tw){
            switch(tw[1]){
                case POS.NN:          // singular noun
                    tw[0] = (tw[0].isAllUpperCase()) ? tw[0] : tw[0].toLowerCase();
                    filteredTerms.push(tw[0]); break;
                case POS.NNS:         // plural noun
                    filteredTerms.push(tw[0].toLowerCase().singularizeNoun());
                    break;
                case POS.NNP:         // proper noun
                    tw[0] = (tagger.wordInLexicon(tw[0].toLowerCase())) ? tw[0].toLowerCase().singularizeNoun() : tw[0];
                    filteredTerms.push(tw[0]); break;
                case POS.JJ:
                    if(keyAdjectives.indexOf(tw[0]) > -1)
                        filteredTerms.push(tw[0]); break;
            }
        });
        return filteredTerms;
    }


    var getDocumentKeywords = function(dIndex) {
        var docKeywords = {};
        // console.log('index = ' + dIndex);
        tfidf.listTerms(dIndex).forEach(function(item){
            if( item.term.toUpperCase().includes('ERROR')) {
                console.log('term =' + item.term);
            }
            if(isNaN(item.term) && parseFloat(item.tfidf) > 0 ) {
                docKeywords[item.term] = item.tfidf;
            }
        });

        // var words = Object.keys(docKeywords).map(function(key){ return key; });
        // console.log(words.join(' -- '));
        return docKeywords;
    }




    /////////////////////////////////////////////////////////////////////////////

    var extractCollectionKeywords = function(collection, documentKeywords, minDocFrequency) {

        minDocFrequency = minDocFrequency ? minDocFrequency : s.minDocFrequency;
        var keywordDict = getKeywordDictionary(collection, documentKeywords, minDocFrequency);

        // get keyword variations (actual terms that match the same stem)
        collection.forEach(function(d){
            d.tokens.forEach(function(token){
                var stem = token.stem();
                if(keywordDict[stem] && stopWords.indexOf(token.toLowerCase()) == -1)
                    keywordDict[stem].variations[token] =
                        keywordDict[stem].variations[token] ? keywordDict[stem].variations[token] + 1 : 1;
            });
        });

        // compute keywords in proximity
        keywordDict = computeKeywordsInProximity(collection, keywordDict);
        var collectionKeywords = [];

        var cleanKeywordDict = {};
        _.keys(keywordDict).forEach(function(kw, i) {
            kw.num_keyphrases = Object.keys(kw.keywordsInProximity).length;
            // get human-readable term for each stem key in the dictionary
            var kw_term = getRepresentativeTerm(keywordDict[kw]);

            if(kw_term !== 'ERROR') {
                // Copy to clean dict only if rep. term isn't ERROR and assign the term to entry in clean dict
                cleanKeywordDict[kw] = keywordDict[kw];
                cleanKeywordDict[kw].term = kw_term;

                // Put keywords in proximity in sorted array
                var proxKeywords = [];
                _.keys(cleanKeywordDict[kw].keywordsInProximity).forEach(function(proxKeyword){
                    var proxKeywordsRepetitions = cleanKeywordDict[kw].keywordsInProximity[proxKeyword];
                    if(proxKeywordsRepetitions >= s.minRepetitionsProxKeywords)
                        proxKeywords.push({ stem: proxKeyword, count: proxKeywordsRepetitions });
                });
                cleanKeywordDict[kw].keywordsInProximity = proxKeywords.sort(function(proxK1, proxK2){
                    if(proxK1.count < proxK2.count) return 1;
                    if(proxK1.count > proxK2.count) return -1;
                    return 0;
                });

                // store each key-value in an array
                collectionKeywords.push(cleanKeywordDict[kw]);
            }
        });
        keywordDict = $.extend(true, {}, cleanKeywordDict);

        // sort keywords in array by document frequency
        collectionKeywords = collectionKeywords.sort(function(k1, k2){
                if(k1.df < k2.df) return 1;
                if(k1.df > k2.df) return -1;
                return 0;
            });
        collectionKeywords.forEach(function(k, i){
            keywordDict[k.stem].index = i;
        });

        return { array: collectionKeywords, dict: keywordDict };
    };



    var getKeywordDictionary = function(_collection, _documentKeywords, _minDocFrequency) {

        var keywordDict = {};
        _documentKeywords.forEach(function(docKeywords, i){

            _.keys(docKeywords).forEach(function(stemmedTerm){
                if(!keywordDict[stemmedTerm]) {
                    keywordDict[stemmedTerm] = {
                        stem: stemmedTerm,
                        term: '',
                        df: 1,
                        num_keyphrases: 0,
                        variations: {},
                        inDocument : [_collection[i].id],
                        keywordsInProximity: {}
                    };
                }
                else {
                    keywordDict[stemmedTerm].df++;
                    keywordDict[stemmedTerm].inDocument.push(_collection[i].id);
                }
            });
        });

        _.keys(keywordDict).forEach(function(keyword){
            if(keywordDict[keyword].df < _minDocFrequency)
                delete keywordDict[keyword];
        });
        return keywordDict;
    };


    var computeKeywordsInProximity = function(_collection, _keywordDict) {
        _collection.forEach(function(d){
            d.tokens.forEach(function(token, i, tokens){

                var current = token.stem();
                if(_keywordDict[current]) {   // current word is keyword

                    for(var j=i-s.maxKeywordDistance; j <= i+s.maxKeywordDistance; j++){
                        var prox = tokens[j] ? tokens[j].stem() : undefined;

                        if(_keywordDict[prox] && current != prox) {
                            //var proxStem = prox.stem();
                            _keywordDict[current].keywordsInProximity[prox] = _keywordDict[current].keywordsInProximity[prox] ? _keywordDict[current].keywordsInProximity[prox] + 1 : 1;
                        }
                    }
                }
            });
        });
        return _keywordDict;
    };


    var getRepresentativeTerm = function(k){

        var keys = _.keys(k.variations);

        if(keys.length == 0)
            return 'ERROR';

        // Only one variations
        if(keys.length == 1)
            return keys[0];

        // 2 variations, one in lower case and the other starting in uppercase --> return in lower case
        if(keys.length == 2 && !keys[0].isAllUpperCase() && !keys[1].isAllUpperCase() && keys[0].toLowerCase() === keys[1].toLowerCase())
            return keys[0].toLowerCase();

        // One variation is repeated >= 75%
        var repetitions = 0;
        for(var i = 0; i < keys.length; ++i)
            repetitions += k.variations[keys[i]];

        for(var i = 0; i < keys.length; ++i)
            if(k.variations[keys[i]] >= parseInt(repetitions * 0.75))
                return keys[i];

        // One variation end in 'ion', 'ment', 'ism' or 'ty'
        for(var i = 0; i < keys.length; ++i)
            if(keys[i].match(/ion$/) || keys[i].match(/ment$/) || keys[i].match(/ism$/) || keys[i].match(/ty$/))
                return keys[i].toLowerCase();

        // One variation matches keyword stem
        if(k.variations[k.stem])
            return k.stem;

        // Pick shortest variation
        var shortestTerm = keys[0];
        for(var i = 1; i < keys.length; i++){
            if(keys[i].length < shortestTerm.length)
                shortestTerm = keys[i];
        }
        return shortestTerm.toLowerCase();
    };



/********************************************************************************************************************************************
*
*   PROTOTYPE
*
*********************************************************************************************************************************************/

    KeywordExtractor.prototype = {
        addDocument: function(document, id) {
            document = (!Array.isArray(document)) ? document : document.join(' ');
            id = id || this.collection.length;
            this.collection.push({ id: id, text: document });
        },
        processCollection: function() {
            tfidf = new natural.TfIdf();
            var timestamp = $.now();
            this.documentKeywords = extractDocumentKeywords(this.collection);
            var collectionKeywords = extractCollectionKeywords(this.collection, this.documentKeywords);
            this.collectionKeywords = collectionKeywords.array;
            this.collectionKeywordsDict = collectionKeywords.dict;

            var miliseconds = $.now() - timestamp;
            var seconds = parseInt(miliseconds / 1000);
            console.log('Keyword extraction finished in ' + seconds + ' seconds, ' + miliseconds%1000 + ' miliseconds (=' + miliseconds + ' ms)');
        },
        listDocumentKeywords: function(index) {
            return this.documentKeywords[index];
        },
        getCollectionKeywords: function() {
            return this.collectionKeywords;
        },
        getCollectionKeywordsDictionary: function() {
            return this.collectionKeywordsDict;
        },
        clear: function() {
            tfidf = null;
            this.collection = [];
            this.documentKeywords = [];
            this.collectionKeywords = [];
            this.collectionKeywordsDict = {};
        }
    };

    return KeywordExtractor;
})();


module.exports = KeywordExtractor;












/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0), __webpack_require__(1)))

/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(_) {var Globals = __webpack_require__(3);
var RSContent = __webpack_require__(10);


var RankingModel = (function() {
    'use strict';


    var _this;
    function RankingModel(config, dataConn){
        this.conf = config;
        this.dataConn = dataConn || null;
        this.clear();
        _this = this;
    }


    /*******************************************
    * Functions
    *******************************************/
    var assignRankingPositionsAndShift = function(_data, _score){
        var currentScore = Number.MAX_VALUE;
        var currentPos = 1;
        var itemsInCurrentPos = 0;
        _data.forEach(function(d, i){
            if(d.ranking[_score] > 0){
                if( d.ranking[_score] < currentScore ){
                    currentPos = currentPos + itemsInCurrentPos;
                    currentScore = d.ranking[_score];
                    itemsInCurrentPos = 1;
                } else{
                    itemsInCurrentPos++;
                }
                d.ranking.pos = currentPos;
            } else{
                d.ranking.pos = 0;
            }
            // shift computation
            d.ranking.posChanged = d.ranking.prev_pos > 0 ? d.ranking.prev_pos - d.ranking.pos : 1000;
        });
        return _data;
    };


    /**
     *	Creates the ranking items with default values and calculates the weighted score for each selected keyword (tags in tag box)
     * */
     // FIX!!!!!!!!!!
    var updateRanking =  function(oldRanking, query, rs_conf){
        var cbWeight = rs_conf.CB.weight; // (score == RANKING_MODE.overall.attr) ? opt.rWeight : 1;
        var tuWeight = rs_conf.TU.weight; // (score == RANKING_MODE.overall.attr) ? (1- opt.rWeight) : 1;
        var score =  rs_conf[rs_conf.rankBy].name;
        var newRanking = oldRanking.slice();
        // MAKE ONE LOOP
        newRanking.forEach(function(d){ d.ranking.prev_pos = d.ranking.pos; });
        if(cbWeight)            
            newRanking = RSContent.getCBScores({ data: newRanking, keywords: opt.query, options: { rWeight: cbWeight } });
        // if(tuWeight)
        //     ranking = _this.tuRS.getTagUserScores({ user: opt.user, keywords: opt.query, data: ranking, options: { rWeight: tuWeight } });
        newRanking.forEach(function(d){
            d.ranking.total_score = 0;
            if(cbWeight)
                d.ranking.total_score += d.ranking.cb_score;
            // if(tuWeight)
            //     d.ranking.total_score += d.ranking.tu_score;
        });

        var secScore = undefined;
        if(score === 'CB' && tuWeight) secScore = rs_conf.TU.name;
        if(score === 'TU' && cbWeight) secScore = rs_conf.CB.name;
        newRanking = newRanking.sort(function(d1, d2){
            if(d1.ranking[score] > d2.ranking[score]) return -1;
            if(d1.ranking[score] < d2.ranking[score]) return 1;
            if(d1.ranking[secScore] && d1.ranking[secScore] > d2.ranking[secScore]) return -1;
            if(d1.ranking[secScore] && d1.ranking[secScore] < d2.ranking[secScore]) return 1;
            return 0;
        });
        newRanking = assignRankingPositionsAndShift(newRanking, score);
        return newRanking;
    };



    var updateStatus =  function(ranking, curStatus) {

        // if(_this.ranking.length === 0)
        //     return Globals.RANKING_STATUS.no_ranking;

        // if(_this.status === Globals.RANKING_STATUS.no_ranking)
        //     return Globals.RANKING_STATUS.new;

        // for(var i in _this.ranking) {
        //     if(_this.ranking[i].ranking.posChanged > 0)
        //         return Globals.RANKING_STATUS.update;
        // }
        if(ranking.length === 0)
            return Globals.RANKING_STATUS.no_ranking;

        if(curStatus === Globals.RANKING_STATUS.no_ranking)
            return Globals.RANKING_STATUS.new;

        for(var i in ranking) {
            if(ranking[i].ranking.pos_changed > 0)
                return Globals.RANKING_STATUS.update;
        }
        return Globals.RANKING_STATUS.unchanged;
    };



    var _setData = function(data) {
        if(this.useLocal) {
            this.status = Globals.RANKING_STATUS.no_ranking;
            this.data = data.slice() || [];
            this.ranking = this.data.slice();
            this.ranking.forEach(function(d){
                d.ranking = {
                    pos: 0,
                    pos_changed: 0,
                    prev_pos: 0,
                    total_core: 0,
                    cb_score: 0,
                    cb_max_score: 0,
                    cb_details: [],
                    tu_score: 0,
                    tu_details: {}
                };
            });
        }
        return this;
    };



    var _update = function(params, onDone) {
        // CONF
        // rs : [
        //     {
        //         name: 'CB',
        //         active: true,
        //         weight : 0.5,
        //         attr : 'keywords'
        //     },
        //     {
        //         name: 'CF',
        //         active: true,
        //         weight : 0.5,
        //         attr : 'neighbors'
        //     }
        // ],
        // rankBy : 'CB'

        // this.query = params.query;
        this.features = params.features;
        this.conf = params.rs_conf;
        this.rankBy = this.conf.rankBy;

        var onRankingUpdated = function(ranking) {
            _this.ranking = ranking;
            _this.status = updateStatus(ranking, _this.status);
            // onDone(this.ranking, _this.status);
            onDone(_this.ranking, _this.status);
        };

        if(this.conf.useLocal) {
            // sync
            // var ranking = this.query.length ? updateRanking(this.ranking, params) : [];
            var ranking = this.features.keywords.length ? updateRanking(this.ranking, params) : [];
            onRankingUpdated(ranking);
        } else { 
            // async
            _this.dataConn.updateRanking(params, function(ranking) {
                onRankingUpdated(ranking);
            });    
        }
    };


    var _reset = function() {
        this.previousRanking = [];
        this.ranking = [];
        this.status = updateStatus();
        this.query = [];
        return this;
    };



    var _clear = function() {        
        this.ranking = [];
        this.data = [];
        this.query = [];
        this.status = Globals.RANKING_STATUS.no_ranking;
        // if(!this.useLocal)
        //     this.dataConn.clearRanking();
        return this;
    };




/****************************************************************************************************
 *
 *   RankingModel Prototype
 *
 ****************************************************************************************************/
    RankingModel.prototype = {
    //return {

        setData: _setData,

        update: _update,

        reset: _reset,

        clear: _clear,

        getRanking: function() {
            // return this.ranking;
            return this.ranking;
        },

        getStatus: function() {
            // return this.status;
            return this.status;
        },

        getOriginalData: function() {
            // return this.data;
            return this.data;
        },

        getQuery: function() {
            // return this.query;
            return this.query;
        },

        getRankingDict: function(){
            var dict = {};
            // this.ranking.forEach(function(d){ dict[d.id] = d; });
            this.ranking.forEach(function(d){ dict[d.id] = d; });
            return dict;
        },

        getMaxTagFrequency: function(){
            return this.tuRS.getmaxSingleTagFrequency();
        },

        getActualIndex: function(index){
            // if(this.status == Globals.RANKING_STATUS.no_ranking)
            //     return index;
            // return this.ranking[index].originalIndex;
            if(this.status == Globals.RANKING_STATUS.no_ranking)
                return index;
            return this.ranking[index].originalIndex;
        },
        getDocumentById: function(id) {
            var getId = function(d){ return d.id === id };
            // return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[_.findIndex(this.data, getId)] : this.ranking[_.findIndex(this.ranking, getId)];
            return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[_.findIndex(this.data, getId)] : this.ranking[_.findIndex(this.ranking, getId)];
        },
        getDocumentByIndex: function(index) {
            // return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[index] : this.ranking[index];
            return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[index] : this.ranking[index];
        }
    };

    return RankingModel;
})();


module.exports = RankingModel;


/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(1)))

/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var Globals = __webpack_require__(3);

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


/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 15 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var DocViewer = (function(){

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
            $contentSectionOuter/*.css('overflowY', 'hidden')*/.mCustomScrollbar(customScrollOptions);
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

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var NeighborsCloud = (function(){

	var _this, $root, $neighborcloud, $tooltip;
	var s;
	var simFeat = {
			'C': 'Co-authorship', 
			'G': 'Geographic Distance', 
			'I': 'Similar Interests', 
			'P': 'Publication Similarity', 
			'S': 'Social Context'
		};

	function NeighborsCloud(params){
		_this = this;
	    s = $.extend({
	        root: '',
	        attr: {},
	        options: {},
	        cb:{
	            onNeighborTagMouseEnter: function(index, id){},
	            onNeighborTagMouseLeave: function(index, id){},
	            onNeighborTagClick: function(index, id){},
	            onNeighborTagSelected: function(index, id){}
	        }
	    }, params);
	    this.neighbors = [];

	   	$root = $(s.root);
	}

	var setTagProperties = function($tag, t, index) {
		$tag.off().on({
				'click': function(evt){
					var tid = '#urank-neighbortag-' + t.neighbor.id;
					var $tag = $(tid)
					if(!$tag.hasClass('selected')) {
						s.cb.onNeighborTagSelected(index, t.neighbor.id);	
					}
				},
				'mouseenter': function(evt){
					s.cb.onNeighborTagMouseEnter(index, t.neighbor.id)
				},
				'mouseleave': function(evt){
					s.cb.onNeighborTagMouseLeave(index, t.neighbor.id)
				}
			})
			.css({
				'color': _this.colors(t.neighbor.name),
				'font-size': (s.options.minFontSize + t.score * s.options.fontSizeGrowth)+'px',
				'background': ''
			});

	}

	var addTooltip = function(tag, $tag){
		$('.tag-tooltip').remove();
		$tooltip = $('<div/>', { id: 'neighbor-tag-tooltip', class: 'tag-tooltip' }).appendTo($root);
	
		var $titleWrapper = $('<div/>', { class: 'title-wrapper' }).appendTo($tooltip);
		$('<div/>', { class: 'title', html: tag.neighbor.name }).appendTo($titleWrapper);
		$('<div/>', { class: 'friend' }).appendTo($tooltip);

		if(tag.explanations.friend)
			var $feat = $('<div/>', { class: 'sim-feature' }).appendTo($tooltip);
			$('<span/>', { name: 'friend', html: 'Friend' }).appendTo($feat)
				.css('font-size', '18px');
		for(feat in simFeat){
			if(simFeat[feat]) {
				var $feat = $('<div/>', { class: 'sim-feature' }).appendTo($tooltip);
				var fontSize = Math.min(6 + tag.explanations[feat] * 8, 20);
				$('<span/>', { name: feat, html: simFeat[feat] }).appendTo($feat)
					.css('font-size', fontSize+'px');	
			}
			
		}

		var height = $tooltip.height();
		var width = $tooltip.width();
		var top = parseInt($tag.offset().top) - height+50;
		var left = parseInt($neighborcloud.offset().left) - width;
		$tooltip.css({ top: top, left: left, width: width });

	};

	var build = function(neighbors, colors){
		this.neighbors = neighbors;
		this.colors = colors;

		$root.addClass('urank-tag-container');
		$container = $('<div/>', { class: 'urank-tag-container-outer'}).appendTo($root);
		$('<div/>', { class: 'urank-hidden-scrollbar' }).appendTo($container)
		$scrollable = $('<div/>').appendTo($container).addClass('urank-hidden-scrollbar-inner')
            // .on('scroll', onRootScrolled);
        $neighborcloud = $('<div/>').appendTo($scrollable).addClass('urank-tag-container-inner');
		// $neighborcloud = $('<div/>', { class: 'urank-tag-container-inner' }).appendTo($scrollable);
		// addTooltip();

		this.neighbors.forEach(function(t, index) {
			var $tag = $('<div/>', {
				id: 'urank-neighbortag-' + t.neighbor.id,
				'class': 'urank-tag',
				'name': t.tag,
				'html': t.neighbor.name
			}).appendTo($neighborcloud);
			// Bind event handlers and set style
			setTagProperties($tag, t, index);
		});
	};


	var selectNeighborTag = function(index, id, color) {
		var $tag = $('#urank-neighbortag-' + id);
		if(!$tag.hasClass('selected')) {
			var $clone = $tag.clone().attr('id', 'urank-neighbortag-'+id+'-clon');
			$tag.after($clone);
			$tag.addClass('selected').css({
				'color': 'white',
				'background': color
			});
		}
	};

	var tooltipTimeout, fadeOutTimeOut;

	var onNeighborTagMouseEntered = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		if(!$tag.hasClass('selected'))
			$tag.addClass('hovered');

		// fill tooltip
		tooltipTimeout = setTimeout(function(){
			var tag = _this.neighbors[index];
			addTooltip(tag, $tag);
			
			$tooltip.fadeIn();
			fadeOutTimeOut = setTimeout(function(){
			    $tooltip.fadeOut();
			}, 4000);
		}, 100);
		
	};


	var onNeighborTagMouseLeft = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		$tag.removeClass('hovered');
		clearTimeout(tooltipTimeout);
        clearTimeout(fadeOutTimeOut);
        if($tooltip)
        	$tooltip.hide();
	};


	var restoreTag = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);		            // is in tagcloud
		var $clonedTag = $('#urank-neighbortag-' + id + '-clon');   // is in tagbox, will be deleted sync
		var $dummyTag = $clonedTag.clone();                     	// need dummy for animation, clone is removed
		$dummyTag.attr('id', 'dummy-tag-' + id);
		console.log('Animating ' + $dummyTag.attr('id'));
		//  Save offset in tagBox before detaching
		var oldOffset = $clonedTag.offset();
		var newOffset = $tag.offset();
		// Detach tag from tag cloud, attach temporarily to body and place it in old position (in tagBox)
		$dummyTag.appendTo('body')
		    .css({ position: 'absolute', top: oldOffset.top, left: oldOffset.left, 'z-index': 9999 });
		// Animate tag moving from tag box to tag cloud
		$dummyTag.animate({ top: newOffset.top, left: newOffset.left }, 800, 'swing', function() {
		    //  Detach from body after motion animation is complete and append to tag container again
		    $dummyTag.remove();
		    $tag.removeClass().addClass('urank-tag'); //.setTagStyle();
		    setTagProperties($tag, _this.neighbors[index], index);
		    // $tag = $tag.detach();
		    // $clonedTag.after($tag);
		    // $clonedTag.remove();
		    // $tag.css({ position: '', top: '', left: '', 'z-index': '' }).setTagStyle();
		    // setTagProperties($tag);
		});

	}

	

	NeighborsCloud.prototype = {
		// init
		build : build,
		// when user selects a tag, node, ot person icon
		selectNeighborTag: selectNeighborTag,
		// mouse over
		onNeighborTagMouseEnter: onNeighborTagMouseEntered,
		// mouse leave
		onNeighborTagMouseLeave: onNeighborTagMouseLeft,
		// when tag deleted in tagbox (box above ranking)
		restoreTag: restoreTag
	};

	return NeighborsCloud;
})()

module.exports = NeighborsCloud;
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var Globals = __webpack_require__(3);
var utils = __webpack_require__(9);

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

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($, _) {// var $ = require('jquery');
// var _ = require('underscore');
var VIEWS = __webpack_require__(4);


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

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0), __webpack_require__(1)))

/***/ }),
/* 19 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($, d3, _) {
__webpack_require__(8);

var TagCloudDefault = (function(){

    var _this;
    // Settings
    var s = {};
    //  Classes
    var tagcloudDefaultClass = 'urank-tagcloud-default',
        hiddenScrollbarClass = 'urank-hidden-scrollbar',
        hiddenScrollbarInnerClass = 'urank-hidden-scrollbar-inner',
        tagContainerClass = 'urank-tagcloud-tag-container',
        tagClass = 'urank-tagcloud-tag',
        activeClass = 'active',
        hoveredClass = 'hovered',
        selectedClass = 'selected',
        disabledClass = 'disabled',
        droppedClass = 'dropped',
        focusedClass = 'focused',
        hiddenClass = 'hidden',
        addableClass = 'addable',
        addedClass = 'added',
        tagHintClass = 'urank-tagcloud-tag-hint',
        keywordHintClass = 'urank-tagcloud-tag-cooccurence-hint',
        documentHintClass = 'urank-tagcloud-tag-document-hint',
        tooltipClass = 'urank-tagcloud-tag-tooltip',
        addIconClass = 'urank-tagcloud-tag-add-icon';
    //  Ids
    var tagIdPrefix = '#urank-tag-',
        tagPiePrefix = '#urank-tag-pie-';
    //   Attributes
    var tagPosAttr = 'tag-pos';
    //  Helpers
    var backgroudGradient = "top, rgb(0, 102, 255), rgb(20, 122, 255), rgb(0, 102, 255)";
    var $root = $(''), $scrollable = $(''), $tagContainer = $(''), $tooltip = $(''),
        tooltipTimeOut, fadeOutTimeOut,

        tagHintPinOptions = {
            document: { top: -6, right: -10, container: '.'+tagcloudDefaultClass },
            cooccurence: { bottom: -10, right: -10, container: '.'+tagcloudDefaultClass }
        },

        pieOptions = {
            size: { pieOuterRadius: '100%', canvasHeight: '14', canvasWidth: '14' },
            effects: {
                load: { effect: "none" },
                pullOutSegmentOnClick: { effect: 'none', speed: 0, size: 0 },
                highlightSegmentOnMouseover: false
            },
            labels: {
                inner: { format: '' },
                lines: { enabled: false}
            },
            data: {
                content: [
                    { label: 'documentsIn', value: 0, color: '#65BA20' },
                    { label: 'documentsNotIn', value: 0, color: '#fafafa' },
                ]
            },
            misc: {
                colors: { segmentStroke: '#65a620' },
                canvasPadding: { top: 0, right: 0, bottom: 0, left: 0 },
                gradient: { enabled: true, percentage: 100, color: "#888" },
            }
        };

    //  Constructor
    function TagCloudDefault(params) {
        _this = this;
        s = $.extend({
            root: '',
            attr: {},
            options: {}, // numCategories, tagStyle
            cb:{
                onTagInCloudMouseEnter: function(index, id){},
                onTagInCloudMouseLeave: function(index, id){},
                onTagInCloudClick: function(index, id){},
                onTagSelected: function(index, id){}    // used when selction == 'click'
            }
        }, params);

        this.keywords = [];
        this.isTagBeingDragged = false;
        this.tagHintMode = false;
        this.selectedTag = undefined;
        this.addedTags = [];
    }

    // jquery function to change tag style
    $.fn.setTagStyle = function() {
        var $tag = $(this);
        var idx = parseInt($tag.attr('tag-pos'));
        var kw = _this.keywords[idx];

        if($tag.hasClass('disabled'))
            return $tag.css({ background: '', border: '' });

        if($tag.hasClass('active') && ($tag.hasClass('hovered') || $tag.hasClass('selected') || $tag.hasClass('added')))
            return $tag.css({ background: '', border: '' });

        // dropped class is always for a cloned tag
        if($tag.hasClass('dropped')) {
            var color = $tag.data('queryColor');
            var border = 'solid 1px ' + color;
            var bg = s.options.highlight === 'background' ? color : 'transparent';
            var fontColor = s.options.highlight === 'background' ? 'white' : kw.color;
            return $tag.css({ 'background': bg, 'border': border, 'color': fontColor });
        }
            
        if($tag.hasClass('active')/* || $tag.hasClass('addable')*/) {
            if(s.options.tagStyle === 'badge') {
                return $tag.addClass('badge').css({
                    background: function() { return getGradientString($tag.data('originalColor')) },
                    border: '',
                });
            } else if(s.options.tagStyle === 'word') {
                // console.log(s.options.minFontSize + s.options.fontSizeGrowth * kw.score);
                return $tag.addClass('word').css({
                    // 'color': kw.color,
                    'color': $tag.data('originalColor'),
                    'font-size': (s.options.minFontSize + s.options.fontSizeGrowth * kw.score) + 'px',
                    'border': '', 'background': ''
                });
            }
        }
            
        return $tag;
    };

    /// Tag Cloud root and container event handlers
    var onRootScrolled = function(event) {
        event.stopPropagation();
        if(_this.tagHintMode)
            pinTagHints($('.'+tagClass+'.'+selectedClass));
    };

    ////////////////////////////////////////////////
    // DRAGGABLE EVENTS AND OPTIONS
    ////////////////////////////////////////////////

    var $draggedTag = undefined;
    var originalOffset = {};

    var draggableEvt = {
        // ON DRAG STARTED
        onTagDragStarted : function(event, ui){
            _this.isTagBeingDragged = true;
            $tooltip.hide();
            clearTimeout(tooltipTimeOut);
            clearTimeout(fadeOutTimeOut);

            $(this).data('dropped', false).data('addedTags', _this.addedTags)
            //.removeClass(hoveredClass)
            //.setTagStyle()
            ;

            $(ui.helper).addClass('dragging');

            $draggedTag = $(this).clone()
                .attr('id', $(this).attr('id') + '-clon')
                .data('originalColor', $(this).data('originalColor'))
                .removeClass('ui-draggable').removeClass('ui-draggable-handle')
                .setTagStyle()
                .hide();
            $(this).after($draggedTag);

            // Start added tag animation
            originalOffset = { top: event.pageY, left: event.pageX };

            $('.'+addedClass).each(function(i, addedTag){
                var $addedTag = $(addedTag);
                var $clonAddedTag = $addedTag.clone()
                    .attr('id', $(this).attr('id') + '-clon')
                    .data('originalColor', $(this).data('originalColor'))
                    .removeClass('ui-draggable').removeClass('ui-draggable-handle')
                    .setTagStyle();

                var tagOffset = $addedTag.position();
                $addedTag.after($clonAddedTag);
                $addedTag.detach()
                .appendTo('body')
                .css({
                    position: 'absolute',
                    left: tagOffset.left,
                    top: tagOffset.top,
                    'z-index': 9999
                });
            });
        },

        // ON DRAGGED
        onTagDragged : function(event, ui){
            var currentOffset = { top: event.pageY - originalOffset.top, left: event.pageX - originalOffset.left };
            originalOffset = { top: event.pageY, left: event.pageX };

            _this.addedTags.forEach(function(tag, i){
                var $addedTag = $(tagIdPrefix + '' + tag.id);
                var tagOffset = $addedTag.position();
                $addedTag.css({ left: tagOffset.left + currentOffset.left, top: tagOffset.top + currentOffset.top });
            });

        },

        // DRAG STOPPED
        onTagDragStopped : function(event, ui){
            _this.isTagBeingDragged = false;
            var $tag = $(this).data('addedTags', '');

            if($tag.data('dropped')) {
                $tag.draggable("destroy");
                $draggedTag.show().removeClass(hoveredClass);
            }
            else {
                $tag.removeClass(hoveredClass).removeClass(disabledClass).setTagStyle();
                $draggedTag.remove();
            }

            //  Added tags
            _this.addedTags.forEach(function(addedTag){
                var $addedTag = $(tagIdPrefix + '' + addedTag.id);
                var $clonAddedTag = $(tagIdPrefix + '' + addedTag.id + '-clon');
                // Restore added tag position
                $addedTag = $addedTag.css({ position: '', left: '', top: '', 'z-index': '' });

                // If dragged tag isn't drop, re-attach added tags and remove clones
                if(!$tag.data('dropped')) {
                    $addedTag = $addedTag.detach();
                    $clonAddedTag.after($addedTag);
                    $clonAddedTag.remove();
                }
            });
            originalOffset = {};
        }

    };


    var draggableOptions = {
        revert: 'invalid',
        helper: 'clone',
        appendTo: '.urank-tagbox-container',
        zIndex: 999,
        start: draggableEvt.onTagDragStarted,
        drag: draggableEvt.onTagDragged,
        stop: draggableEvt.onTagDragStopped
    };

    ////////////////////////////////////////////////
    // End DRAGGABLE EVENTS AND OPTIONS
    ////////////////////////////////////////////////



    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Internal functions

    var extendKeywordsWithColorCategory = function(keywords, numCategories){

        var extent = d3.extent(keywords, function(k){ return k.df; });
        var range = (extent[1] - 1) * 0.1;   // / TAG_CATEGORIES;

        keywords.forEach(function(k){
            var colorCategory = parseInt((k.df - 1/*extent[0]*/) / range);
            k['colorCategory'] = (colorCategory < numCategories) ? colorCategory : numCategories - 1;
        });
        return keywords;
    };


    var pinTagHints = function($tag) {
        $tag.find('.'+documentHintClass).css('visibility', 'visible').pin(tagHintPinOptions.document);
        $tag.find('.urank-doc-hint').pin(tagHintPinOptions.document);
    };


    var setTagProperties = function($tag) {
        var index = $tag.attr(tagPosAttr);
        var id = $tag.attr('tag-id');
        $tag.off().on({
            mousedown : function(event){ if(event.which == 1) event.stopPropagation(); },
            mouseenter: function(event){ s.cb.onTagInCloudMouseEnter(index, id) },
            mouseleave: function(event){ s.cb.onTagInCloudMouseLeave(index, id) },
            click: function(event){ _tagClicked(index, id) }
        });
    
        // if it's not clon of dropped tag, add class active and make it drggable
        if(!$tag.hasClass(droppedClass)) {
            // Set default style
            $tag.addClass(activeClass);
            // Set draggable if selection = 'drag'
            if(s.options.selection === 'drag') {
                if($tag.is('.ui-draggable'))
                    $tag.draggable('destroy');
                $tag.draggable(draggableOptions);    
            }
        } 
        // if ($tag.hasClass(hiddenClass))
        //     $tag.hide();    
    
        // Reset hints visibility
        $tag.find('.'+documentHintClass).css('visibility', '')
    
        return $tag.setTagStyle();
    };



    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype methods

    /**
    * * @param {array of objects} keywords Description
    */
    var _build = function(keywords, data, colorScale){
        this.keywords = extendKeywordsWithColorCategory(keywords.slice(), s.options.numCategories);
        this.data = data;
        this.colorScale = colorScale;

        // Empty tag container and add appropriate class/es
        $root = $(s.root).empty().addClass(tagcloudDefaultClass);

        $tooltip = $('<div/>').appendTo($root).addClass(tooltipClass).width($root.width() - 10);
        // $("<p><strong name='num-docs'></strong> items contain</p>").appendTo($tooltip);
        // // $("<p><strong name='num-docs'></strong> (<strong name='pctg-docs'></strong>) documents contain</p>").appendTo($tooltip);
        // $("<p><strong name='tag'></strong></p>").appendTo($tooltip);
        // // $("<p>Appears in <strong name='num-kw'></strong> phrases</p>").appendTo($tooltip);
        // // $("<p><strong name='num-kw'></strong> other keywords in proximity</p>").appendTo($tooltip);

        $("<p><strong name='tag'></strong></p>").appendTo($tooltip);
        $("<p>appears in <strong name='num-docs'></strong> items</p>").appendTo($tooltip);

        $tooltip.css('top', $root.position().top - $tooltip.fullHeight()).hide();

        $('<div/>').appendTo($root).addClass(hiddenScrollbarClass);

        $scrollable = $('<div/>').appendTo($root).addClass(hiddenScrollbarInnerClass)
            .on('scroll', onRootScrolled);
        $tagContainer = $('<div/>').appendTo($scrollable).addClass(tagContainerClass);

        this.keywords.forEach(function(k, i){
            // Append tag
            k.color = _this.colorScale(k.colorCategory);
            var $tag = $('<div/>', { 
                'id': 'urank-tag-' + k.id, 
                'tag-id': k.id || i,
                'tag-pos': i,
                'name': k.term 
            }).appendTo($tagContainer)
                .addClass(tagClass + ' ' + activeClass/* + ' hint--info hint--left'*/)
                .data({ 
                    'originalColor': _this.colorScale(k.colorCategory)
                })
                .html(k.term)
                .hide()
                .fadeIn((i+1)*20);
            // Pie chart section for document hint
            // var docPctg = parseInt((k.df * 100) / _this.data.length);
            // if(docPctg > 0 && docPctg < 5) { docPctg = 5; }
            // else {
            //     if(docPctg%5 < 3) docPctg = docPctg - docPctg%5;
            //     else docPctg = docPctg + 5 - docPctg%5;
            // }
            // var $docHint = $('<a/>', { class: 'urank-doc-hint urank-doc-hint-'+docPctg, href: '#' }).appendTo($tag);
//            var $docHint = $('<div/>', { class: tagHintClass+' '+documentHintClass, id: 'urank-tag-pie-' + i }).appendTo($tag);
//            pieOptions.data.content[0].value = k.df;
//            pieOptions.data.content[1].value = _this.data.length - k.df || 0.1;
//            var tagPie = new d3pie(tagPiePrefix+''+i, pieOptions);
            // Red circle for keywords in proximity hint
            if(k.num_keyphrases)
                // $('<a/>', { class: keywordHintClass, 'data-content': k.num_keyphrases, href: '#' }).appendTo($tag);
                $('<a/>', { class: keywordHintClass, 'data-content': k.df, href: '#' }).appendTo($tag);
            // Add/remove icon
            $('<a/>', { href: '#' }).appendTo($tag).addClass(addIconClass);
            setTagProperties($tag);
        });
        return this;
    };



    var _reset = function() {
        return this.build(this.keywords, this.data, this.colorScale, s.options);
    };


    var _hoverTag = function(index, id) {
        var $tag = $(tagIdPrefix + '' + id);
        if(!_this.tagHintMode && !_this.isTagBeingDragged) {
            if(!$tag.hasClass(droppedClass))
                $tag.addClass(hoveredClass).setTagStyle();
                    //.css(tagStyle.hover);
            pinTagHints($tag);
            tooltipTimeOut = setTimeout(function(){
                $tooltip.find("[name='num-docs']").html(_this.keywords[index].df);
                $tooltip.find("[name='pctg-docs']").html(Math.floor(_this.keywords[index].df/_this.data.length * 100) + '%');
                $tooltip.find("[name='tag']").html(_this.keywords[index].term.toUpperCase());
                $tooltip.find("[name='num-kw']").html(_this.keywords[index].num_keyphrases);
                $tooltip.fadeIn();
                fadeOutTimeOut = setTimeout(function(){
                    $tooltip.fadeOut();
                }, 4000);
            }, 500);
        }
    };


    var _unhoverTag = function(index, id) {
        var $tag = $(tagIdPrefix + '' + id);

        if(!_this.tagHintMode && !_this.isTagBeingDragged) {
            $tag.find('.'+documentHintClass).css('visibility', '');
            //if(!$tag.hasClass(droppedClass)) {
                $tag.removeClass(hoveredClass).setTagStyle();
            //}
            clearTimeout(tooltipTimeOut);
            clearTimeout(fadeOutTimeOut);
            $tooltip.hide();
        }
    };


    var _tagClicked = function(index, id) {
        var $tag = $(tagIdPrefix + '' + id);

        if (s.options.selection === 'click' && !$tag.hasClass(droppedClass)) {
            $clonTag = $tag.clone().attr('id', $tag.attr('id') + '-clon')
                //.addClass('dropped');//.setTagStyle(); //change color for background
                //css({ 'color': 'white', 'background-color': $tag.data('originalColor')});
            $tag.after($clonTag).addClass('dropped');
            s.cb.onTagSelected(index, id); // will append tag to tagbox and restyle clon here
            return;
        }

        if(s.options.selection === 'drag' && !_this.isTagBeingDragged) {
            // Add or remove tag from this.addedTags for multiple selection
            if(_this.selectedTag) {
                if($tag.hasClass(addableClass)) {
                    // _this.addedTags.push($tag.attr(tagPosAttr));
                    _this.addedTags.push({ 'index': index, 'id': id });
                    $tag.addClass(addedClass).removeClass(addableClass).setTagStyle();
                }
                else if($tag.hasClass(addedClass)) {
                    // _this.addedTags.splice(_this.addedTags.indexOf($tag.attr(tagPosAttr)), 1);
                    indexToExclude = _.findIndex(_this.addedTags, function(tag) {
                        return tag.id == id;
                    })
                    _this.addedTags.splice(indexToExclude, 1);
                    $tag.addClass(addableClass).removeClass(addedClass).setTagStyle();                    
                }
            }
            // 
            else {
                s.cb.onTagInCloudClick(index, id);  // so that urank shows/hides items in the list and ranking
                _this.selectedTag = index;
                $tag.addClass(selectedClass).removeClass(hiddenClass).setTagStyle();

                if(!$tag.hasClass(droppedClass)) {
                    if($tag.is('.ui-draggable'))
                        $tag.draggable('destroy');
                    $tag.draggable(draggableOptions);
                }

                // SIBLINGS
                var proxKeywords = _this.keywords[index].keywordsInProximity || {};
                $tag.siblings().each(function(i, sibling){

                    var $siblingTag = $(sibling);
                    if($siblingTag.is('.ui-draggable'))
                        $siblingTag.draggable('destroy');

                    $siblingTag.find('.'+documentHintClass).off().css('visibility', 'hidden');

                    // sibling tags that are not KW in proximity of current tag are dimmend and active class removed so they can't be dragged
                    if(_.findIndex(proxKeywords, function(proxKw){ return proxKw.id == $siblingTag.attr('tag-id') }) === -1) {
                        $siblingTag.addClass(disabledClass).removeClass(activeClass).setTagStyle();
                    }
                    else {                                      // Active tags are the ones co-occuring with the selected tag. A tooltip is added during proxKeywordsmode
                        if(!$siblingTag.hasClass(droppedClass)) {
                            $siblingTag.addClass(activeClass).addClass(addableClass);
                            $siblingTag.show();
                        }
                    }
                    pinTagHints($tag);
                });
                _this.tagHintMode = true;
            }
        } 
    };


    /**
	 *	Detach tag from tag box and return it to container (tag cloud)
	 *
	 * */
    var _restoreTag = function(index, id){

        var $tag = $(tagIdPrefix + '' + id);                    // is in tagcloud
        var $clonedTag = $(tagIdPrefix + '' + id + '-clon');    // is in tagbox, will be deleted sync
        var $dummyTag = $clonedTag.clone();                     // need dummy for animation, clone is removed
        $dummyTag.attr('id', 'dummy-tag-' + id);
        console.log('Animating ' + $dummyTag.attr('id'));
        //  Save offset in tagBox before detaching
        var oldOffset = $clonedTag.offset();
        var newOffset = $tag.offset();
        // Detach tag from tag cloud, attach temporarily to body and place it in old position (in tagBox)
        $dummyTag.appendTo('body')
            .css({ position: 'absolute', top: oldOffset.top, left: oldOffset.left, 'z-index': 9999 });
        // Animate tag moving from tag box to tag cloud
        $dummyTag.animate({ top: newOffset.top, left: newOffset.left }, 800, 'swing', function() {
            //  Detach from body after motion animation is complete and append to tag container again
            $dummyTag.remove();
            $tag.removeClass().addClass(tagClass + ' ' + activeClass); //.setTagStyle();
            setTagProperties($tag);
            // $tag = $tag.detach();
            // $clonedTag.after($tag);
            // $clonedTag.remove();
            // $tag.css({ position: '', top: '', left: '', 'z-index': '' }).setTagStyle();
            // setTagProperties($tag);
        });
    };


    var _focusTag = function(keyword/*, newOffset*/) {
        var $tag = $('.'+tagClass + '[tag-pos=' + keyword.index + ']');
        $tag.addClass(focusedClass).removeClass(hiddenClass); //.show();

        setTimeout(function(){
            $tag.removeClass(focusedClass, 2000);
        }, 5000);

        $scrollable.scrollTo('.'+tagClass + '[tag-pos=' + keyword.index + ']', { offsetTop: 10 });
        return this;
    };


    var _updateClonOfDroppedTag = function(index, id, queryColor) {
        var $tag = $(tagIdPrefix + '' + id)
            .data('queryColor', queryColor)
            .removeClass(activeClass).removeClass(disabledClass).removeClass(selectedClass)
            .addClass(droppedClass);
        $tag.setTagStyle();
        // setTagProperties($tag);
        return this;
    };



    var _showTagsWithinRange = function(min, max) {
        _this.keywords.forEach(function(k, i){
            // class selector before id selector avoids hiding tags in tagbox. cloned tags remain visible
            var $tag = $('.'+tagClass + '' + tagIdPrefix + '' + i);

            if(k.df >= min && k.df <= max)
                $tag.removeClass(hiddenClass); //.show();
            else
                $tag.addClass(hiddenClass); //.hide();
        });
    };

    var _clearEffects = function() {

        _this.selectedTag = undefined;
        _this.addedTags = [];
        if(_this.tagHintMode) {
            $('.'+tagClass).each(function(i, tag){
                var $tag = $(tag);
                $tag.removeClass(disabledClass).removeClass(selectedClass).removeClass(hoveredClass).removeClass(addedClass).removeClass(addableClass)
                setTagProperties($tag);
            });
            _this.tagHintMode = false;
        }
        return this;
    };



    var _clear = function() {
        $root.empty();
        return this;
    };


    var _destroy = function() {
        $root.empty();
        return this;
    };


    TagCloudDefault.prototype = {
        build: _build,
        reset: _reset,
        restoreTag: _restoreTag,
        hoverTag: _hoverTag,
        tagClicked:_tagClicked,
        unhoverTag: _unhoverTag,
        focusTag: _focusTag,
        updateClonOfDroppedTag: _updateClonOfDroppedTag,
        showTagsWithinRange: _showTagsWithinRange,
        clearEffects: _clearEffects,
        clear: _clear,
        destroy: _destroy
    };

    return TagCloudDefault;
})();

module.exports = TagCloudDefault;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0), __webpack_require__(2), __webpack_require__(1)))

/***/ }),
/* 20 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var UsertagBox = (function(){

	var _this, $root, $usertagbox;
	var usertags, s;

	function UsertagBox(params){
		_this = this;
	    s = $.extend({
	        root: '',
	        attr: {},
	        options: {},
	        cb:{
	            onUsertagMouseEnter: function(index, id){},
	            onUsertagMouseLeave: function(index, id){},
	            onUsertagClick: function(index, id){},
	            onUsertagSelected: function(index, id){}
	        }
	    }, params);
	    this.usertags = [];

	   	$root = $(s.root);
	}

	var build = function(usertags, colors){
		this.usertags = usertags;

		$root.attr('class', 'urank-usertagbox');
		$usertagbox = $('<div/>', { class: 'urank-usertagbox-inner' }).appendTo($root);

		this.usertags.forEach(function(t, index) {
			var $tag = $('<div/>', {
				id: 'urank-usertag-' + t.id,
				'utag-id': t.id,
				'utag-pos': index,
				'class': 'urank-usertag',
				'name': t.tag,
				'html': t.tag
			}).appendTo($usertagbox);
			// Bind event handlers and set style
			$tag.off()
				.on({
					'click': function(evt){
						s.cb.onUsertagSelected(index, t.id);
					},
					'mouseenter': function(evt){
						s.cb.onUsertagMouseEnter(index, t.id)
					},
					'mouseleave': function(evt){
						s.cb.onUsertagMouseLeave(index, t.id)
					}
				})
				.css({
					'color': colors(t.tag),
					'font-size': (s.options.minFontSize + t.count * s.options.fontSizeGrowth)+'px'	
				});

		});
	};


	var selectUsertag = function(index, id, color) {
		var $tag = $('#urank-usertag-' + id);
		var $clone = $tag.clone().attr('id', 'urank-usertag-'+id+'-clon');
		$tag.after($clone);
		$tag.addClass('selected').css({
			'color': 'white',
			'background': color
		});
	};


	var onUsertagMouseEntered = function(index, id){
		var $tag = $('#urank-usertag-' + id);
		if(!$tag.hasClass('selected'))
			$tag.addClass('hovered');
	};

	var onUsertagMouseLeft = function(index, id){
		var $tag = $('#urank-usertag-' + id);
		$tag.removeClass('hovered');
	};


	

	UsertagBox.prototype = {
		build : build,
		selectUsertag: selectUsertag,
		onUsertagMouseEnter: onUsertagMouseEntered,
		onUsertagMouseLeave: onUsertagMouseLeft
	};

	return UsertagBox;
})()

module.exports = UsertagBox;
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 21 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($, _) {var VIEWS = __webpack_require__(4);

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

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0), __webpack_require__(1)))

/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($, d3) {
var Globals = __webpack_require__(3);

var Ranking = (function(){

    var RANKING = {};
    var s, _this;
    var width, height, margin;
    var x, y, color, xAxis, yAxis, xUpperLimit;
    var svg;
    var data;
    var $root = $('');

    //  Classes
    var svgClass = 'urank-ranking-svg',
        axisClass = 'urank-ranking-axis',
        xClass = 'urank-ranking-x',
        xAxisLabelClass = 'urank-ranking-label',
        yClass = 'urank-ranking-y',
        stackedbarClass = 'urank-ranking-stackedbar',
        backgroundClass = 'urank-ranking-background',
        lightBackgroundClass = 'urank-ranking-light-background',
        darkBackgroundClass = 'urank-ranking-dark-background',
        selectedClass = 'selected',
        dimmedClass = 'dimmed',
        barClass = 'urank-ranking-bar',
        tuSectionClass = 'urank-tag-user-section';

    // Id
    var stackedbarPrefix = '#urank-ranking-stackedbar-';

    function Ranking(params) {
        _this = this;
        s = $.extend({
            root: '.urank-viscanvas-container',
            attr : {},
            options : {
                aes: {
                    lightBackgroundColor: '',
                    darkBackgroundColor: ''
                }
            },
            cb : {
                onItemClicked: function(doc, i){},
                onItemMouseEnter: function(doc, i){},
                onItemMouseLeave: function(doc, i){}
            }
        }, params);
        this.isRankingDrawn = false;
        this.selectedItem = null;
    }

    RANKING.Settings = {
        getExtendedData: function(params){
            var ranking = params.ranking.slice();
            var features = params.features;
            var conf = params.conf;
            var rankBy = params.conf.rankBy;
            var a = [];
            var colors = {};
            // Get tag name -> color mapping
            for(var fkey in features) {
                features[fkey].forEach(function(tag){
                    colors[tag.name] = tag.color;
                })
            }

            ranking.forEach(function(d, i) {
                d.bars = [];
                var x0 = 0.0;
                conf.rs.forEach(function(rs, j) {
                    if(rs.active) {
                        var RS = rs.name;
                        // x0 = rankBy === 'overall' ? x0 : j;
                        d.ranking[RS].details.forEach(function(item) {
                            var x1 = x0 + item.score; 
                            d.bars.push({
                                desc: item.name,
                                x0: x0,
                                x1: x1,
                                color: colors[item.name]
                            });
                            x0 = x1;
                        });
                        // update baseline x0 for next RS
                        x0 = rankBy === 'overall' ? x0 : j+1;
                    }
                });
                a.push(d);
            });
            return a;
        },
        getXUpperLimit: function(conf) {
            if(conf.rankBy === 'overall')
                return 1.0;
            var x_limit = conf.rs.filter(function(rs){ return rs.active }).length;
            return x_limit;
        }
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    RANKING.Evt = {};


    RANKING.Evt.itemClicked = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemClicked.call(this, d[s.attr.id], i);
    };

    RANKING.Evt.itemMouseEntered = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemMouseEnter.call(this, d[s.attr.id], i);
    };

    RANKING.Evt.itemMouseLeft = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemMouseLeave.call(this, d[s.attr.id], i);
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    RANKING.Render = {

        /******************************************************************************************************************
        *
        *	Draw ranking at first instance
        *
        * ***************************************************************************************************************/
        drawNew: function(data, containerHeight){
            margin = { top: 0, bottom: 0, left: 0, right: 0 };
            width = $root.width() - margin.left - margin.right;
            height = containerHeight;
            xUpperLimit = 1;

            // Define scales
            x = d3.scale.linear()
                .domain([0, xUpperLimit])
                .rangeRound( [0, width] );

            y = d3.scale.ordinal()
                .domain(data.map(function(d){ return d[s.attr.id]; }))
                .rangeBands( [0, height]);

            // Define axis' function
            xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .tickValues('');

            yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickValues("");

            // Draw chart main components
            //// Add svg main components
            svg = d3.select(s.root).append("svg")
                .attr("class", svgClass)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("width", width)
                .attr("height", height)
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("g")
                .attr("class", xClass + ' ' + axisClass)
                .attr("transform", "translate(0," + (height) + ")")
                .call(xAxis)
                .selectAll('text');

            svg.append("g")
                .attr("class", yClass +' '+axisClass)
                .call(yAxis)
                .selectAll("text");

            var stackedBars = svg.selectAll('.'+stackedbarClass)
            .data(data).enter()
            .append("g")
            .attr("class", stackedbarClass)
            .attr("id", function(d){ return "urank-ranking-stackedbar-" + d[s.attr.id]; })
            .attr( "transform", function(d) {return "translate(0, " + y(d[s.attr.id]) + ")"; })
            .on('click', RANKING.Evt.itemClicked)
            .on('mouseover', RANKING.Evt.itemMouseEntered)
            .on('mouseout', RANKING.Evt.itemMouseLeft);

            stackedBars.append('rect')
                .attr('class', function(d, i){ return (i%2) ? backgroundClass+' '+darkBackgroundClass : backgroundClass+' '+lightBackgroundClass; })
                .attr('x', 0)
                .attr('width', width)
                .attr('height', y.rangeBand())
                .style('fill', function(d, i){
                if(s.options.aes.lightBackgroundColor != '' && s.options.aes.darkBackgroundColor != '') {
                    if(i%2) return s.options.aes.darkBackgroundColor;
                    return s.options.aes.lightBackgroundColor;
                }
                return  '';
            });
            return this;
        },

        /******************************************************************************************************************
        *
        *	Redraw updated ranking and animate with transitions to depict changes
        *
        * ***************************************************************************************************************/
        redrawUpdated: function(params){
            data = RANKING.Settings.getExtendedData(params);   //(params.ranking, ranking_conf, params.colorScale);
//            width = $root.width();
            RANKING.Render.updateCanvasDimensions(params.listHeight);

            // Redefine x & y scales' domain
            d3.select(s.root).select('.'+svgClass).attr("width", width)
            svg.attr("width", width);

            // xUpperLimit =  data[0].ranking.total_score * 2.0;
            xUpperLimit =  RANKING.Settings.getXUpperLimit(params.conf);
            x.rangeRound( [0, width] ).domain([0, xUpperLimit]).copy();

//            y.rangeBands( [0, height], .02);
            y.rangeBands( [0, height]);
            y.domain(data.map(function(d){ return d[s.attr.id] })).copy();

            var transition = svg.transition().duration(750);
            var delay = function(d, i) { return i * 50; };

            transition.select('.'+xClass+'.'+axisClass).call(xAxis)
                .selectAll("g").delay(delay);

            transition.select('.'+yClass+'.'+axisClass).call(yAxis)
                .selectAll("g").delay(delay);

            RANKING.Render.drawStackedBars();

            ////////////////////////////////////////
            // CHECK IF THIS NEEDS TO BE ENABLED!!
            ////////////////////////////////////////
            // if(opt.ranking.social)
            //     RANKING.Render.drawTagsAndUsersHints(rankingModel.getQuery(), rankingModel.getMaxTagFrequency());

            return this;
        },



        /******************************************************************************************************************
        *
        *	Draw stacked bars either on draw or update methods. Animate with width transition
        *
        * ***************************************************************************************************************/
        drawStackedBars: function(){
            svg.selectAll('.'+stackedbarClass).data([]).exit();
            svg.selectAll('.'+stackedbarClass).remove();
            //svg.selectAll('.'+stackedbarClass).data(data).enter();

            setTimeout(function(){

                var stackedBars = svg.selectAll('.'+stackedbarClass)
                    .data(data).enter()
                    .append("g")
                    .attr("class", stackedbarClass)
                    .attr("id", function(d){ return "urank-ranking-stackedbar-" + d[s.attr.id]; })
                    .attr( "transform", function(d) {return "translate(0, " + y(d[s.attr.id]) + ")"; })
                    .on('click', RANKING.Evt.itemClicked)
                    .on('mouseover', RANKING.Evt.itemMouseEntered)
                    .on('mouseout', RANKING.Evt.itemMouseLeft);

                stackedBars.append('rect')
                    .attr('class', function(d, i){ return (i%2) ? backgroundClass+' '+darkBackgroundClass : backgroundClass+' '+lightBackgroundClass; })
                    .attr('x', 0)
                    .attr('width', width)
                    .attr('height', y.rangeBand())
                    .style('fill', function(d, i){
                        if(s.options.aes.lightBackgroundColor != '' && s.options.aes.darkBackgroundColor != '') {
                            if(i%2) return s.options.aes.darkBackgroundColor;
                            return s.options.aes.lightBackgroundColor;
                        }
                        return  '';
                    });

                stackedBars.selectAll('.'+barClass)
                    .data(function(d) { return d.bars })
                    .enter()
                    .append("rect")
                    .attr("class", barClass)
                    .attr("height", y.rangeBand())
                    .attr("x", function(d) { return x(d.x0); })
                    .attr("width", 0)
                    .attr('transform', 'translate(0, 0.2)')
                    .style("fill", function(d) { return d.color; });

                var bars = stackedBars.selectAll('.'+barClass);

                var getBarWidth = function(d) {
                    var barWidth = x(d.x1) - x(d.x0) - 0.2;
                    return barWidth > 0 ? barWidth : 0;    
                }
                
                var t0 = bars.transition()
                    .duration(800)
                    .attr({ 'width': function(d) { return getBarWidth(d) } });

            }, 800);
            return this;
        },

        /******************************************************************************************************************
        *
        *	Draw minimal views for tag- and user-based recommendations
        *
        * ***************************************************************************************************************/
        drawTagsAndUsersHints: function(query, maxTagFreq) {

            setTimeout(function(){

                var tagHintWidth = query.length * 6 + 6;
                var userHintWidth = 24;
                var xTagHintOffset = x(xUpperLimit) - tagHintWidth - userHintWidth;
                var xUserHintOffset = x(xUpperLimit) - userHintWidth;
                var maxBarHeight = y.rangeBand();

                // Define scales
                var xTU = d3.scale.ordinal().domain(query.map(function(q){ return q.stem; })).rangeBands( [0, tagHintWidth-6], .2);
                var yTU = d3.scale.linear().domain([0, maxTagFreq]).rangeRound([maxBarHeight, 0]);

                // Define axis' function
                var xAxisTU = d3.svg.axis().scale(xTU).orient("bottom").tickValues('');
                var yAxisTU = d3.svg.axis().scale(yTU).orient("left").tickValues('');

                var stackedbars = svg.selectAll('.'+stackedbarClass);

                var tagHints = stackedbars.append('g')
                    .attr('width', tagHintWidth)
                    .attr('height', maxBarHeight)
                    .attr("transform", function(d, i){ "translate(" + xTagHintOffset + "," + y(i) + ")" });

                // draw x axis
                tagHints.append('g')
                    .attr('class', xClass + ' ' + axisClass)
                    .attr('width', xTU.rangeBand())
                    .attr('transform', function(d, i){ return 'translate(' + xTagHintOffset + ',' + maxBarHeight + ')' })
                    .call(xAxisTU)
                    .selectAll('text');

                // draw y axis
                tagHints.append('g')
                    .attr('class', yClass + ' ' + axisClass)
                    .attr('height', maxBarHeight)
                    .attr('transform', function(d, i){ return 'translate(' + xTagHintOffset + ',0)' })
                    .call(yAxisTU)
                    .selectAll('text');

                // draw vertical tag bars
                tagHints.selectAll('.tag-bar')
                    .data(function(d) { return d.tags })
                    .enter()
                    .append("rect")
                    .attr("class", 'tag-bar')
                    .attr("x", function(t) { return xTagHintOffset + xTU(t.stem); })
                    .attr("width", xTU.rangeBand())
                    .attr("y", function(t) { return yTU(t.tagged); })
                    .attr("height", function(t){ return maxBarHeight - yTU(t.tagged); })
                    .style("fill", function(t) { return t.color; });

                // draw user hint
                var userHints = stackedbars.append('g')
                    .attr('class', 'urank-ranking-user-hint')
                    .attr('transform', function(d, i){ 'translate(' + xUserHintOffset + ',' + y(i) + ')' });

                userHints.append('svg:image')
                    .attr('xlink:href', function(d){ return d.ranking.tuMisc.users > 0 ? '../media/user.png' : '' })
                    .attr('x', xUserHintOffset)
                    .attr('width', 13)
                    .attr('y', 12)
                    .attr('height', 13)

                userHints.append('text')
                    .attr('dx', xUserHintOffset + 9)
                    .attr('dy', 15)
                    .text(function(d){ return d.ranking.tuMisc.users > 0 ? d.ranking.tuMisc.users : '' });

            }, 801);

            return this;
        },

        /******************************************************************************************************************
        *
        *	Create drop shadow for click effect on bars
        *
        * ***************************************************************************************************************/
        createShadow: function(){
            // filters go in defs element
            var defs = svg.append("defs");
            // create filter with id #drop-shadow
            // height=130% so that the shadow is not clipped
            var filter = defs.append("filter")
            .attr("id", "drop-shadow")
            .attr("height", "130%");
            // SourceAlpha refers to opacity of graphic that this filter will be applied to
            // convolve that with a Gaussian with standard deviation 3 and store result
            // in blur
            filter.append("feGaussianBlur")
                .attr("in", "SourceAlpha")
                .attr("stdDeviation", 2)
                .attr("result", "blur");
            // translate output of Gaussian blur to the right and downwards with 2px
            // store result in offsetBlur
            filter.append("feOffset")
                .attr("in", "blur")
                .attr("dx", 0)
                .attr("dy", 2)
                .attr("result", "offsetBlur");
            // overlay original SourceGraphic over translated blurred opacity by using
            // feMerge filter. Order of specifying inputs is important!
            var feMerge = filter.append("feMerge");
            feMerge.append("feMergeNode").attr("in", "offsetBlur")
            feMerge.append("feMergeNode").attr("in", "SourceGraphic");
            return this;
        },

        /******************************************************************************************************************
        *
        *	Create drop shadow for click effect on bars
        *
        * ***************************************************************************************************************/
        createBarHoverGradient: function(){
            var defs = svg.append("defs");
            var linearGradient = defs.append('linearGradient').attr('id', 'bar-shadow').attr('x1', '0%').attr('y1', '0%').attr('x2', '0%').attr('y2', '100%');
            // linearGradient.append('stop').attr('offset', '25%').style('stop-color', 'rgba(150,150,150,0.3)');
            // linearGradient.append('stop').attr('offset', '75%').style('stop-color', 'rgba(150,150,150,0.6)');
            // linearGradient.append('stop').attr('offset', '100%').style('stop-color', 'rgba(150,150,150,0.3)');
            linearGradient.append('stop').attr('offset', '100%').style('stop-color', 'rgba(200,200,200,1)');
            return this;
        },

        /*****************************************************************************************************************
        *
        *	Adjust height of svg and other elements when the ranking changes
        *
        * ***************************************************************************************************************/
        updateCanvasDimensions: function(listHeight){
            height = listHeight;
            y.rangeBands(height, .01);

            d3.select(svg.node().parentNode)    // var svg = svg > g
                .attr('height', height + margin.top + margin.bottom);

            svg.attr("height", height + 30)
                .attr("transform", "translate(" + (margin.left) + ", 0)");

            // update axes
            svg.select('.'+xClass+'.'+axisClass).attr("transform", "translate(0," + (height) + ")").call(xAxis.orient('bottom'));
            return this;
        },

        /*****************************************************************************************************************
        *
        *	Redraw without animating when the container's size changes
        *
        * ***************************************************************************************************************/
        resizeCanvas: function(containerHeight) {

            //  Resize container if containerHeight is specified
            if(containerHeight)
                $root.css('height', containerHeight);

            //  Recalculate width
            width = $root.width() - margin.left - margin.right;

            x.rangeRound([0, width]);
            y.rangeBands(height, .02);

            d3.select(svg.node().parentNode).attr('width', width + margin.left + margin.right);
            svg.attr("width", width);

            svg.selectAll('.' + darkBackgroundClass)
                .attr('width', width)
            svg.selectAll('.' + lightBackgroundClass)
                .attr('width', width)

            // update x-axis
            svg.select('.'+xClass + '.'+axisClass).call(xAxis.orient('bottom'));

            // Update bars
            svg.selectAll('.'+stackedbarClass).attr('width', width);
            svg.selectAll('rect.'+backgroundClass).attr('width', width);

            svg.selectAll('.'+barClass)
                .attr("x", function(d) { return x(d.x0); })
                .attr("width", function(d) { return x(d.x1) - x(d.x0); });
            return this;
        }
    };

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype methods

    var _build = function(data, containerHeight) {
        $root = $(s.root);
        _this.originalData = data;
        _this.originalHeight = containerHeight;
        RANKING.Render.drawNew(data, containerHeight).createBarHoverGradient();
        return this;
    }


    var _update = function(params){
        var updateFunc = {};
        updateFunc[Globals.RANKING_STATUS.new] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.update] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.unchanged] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.no_ranking] = _this.reset;
        updateFunc[params.status].call(this, params);
        return this;
    };

    var _clear = function(){
        this.isRankingDrawn = false;
        $root.empty();
        return this;
    };


    var _reset = function() {
        _this.clear();
        _this.build(_this.originalData, _this.originalHeight);
        return this;
    };

    var _selectItem = function(id, index){
        _this.selectedItem = id;
        svg.selectAll('.'+stackedbarClass).style('opacity', 0.2);
        svg.select(stackedbarPrefix + '' + id).style('opacity', 1).select('.'+backgroundClass).style('fill', 'rgba(150,150,150,.5)');
        return this;
    };

    var _highlightItems = function(ids) {
        svg.selectAll('.'+stackedbarClass).style('opacity', function(d){ return (ids.indexOf(d[s.attr.id]) > -1) ? 1 : 0.2 });
        return this;
    };


    var _deSelectAllItems = function(){
        _this.selectedItem = undefined;
        svg.selectAll('.'+stackedbarClass).style('opacity', '')
            .select('.'+backgroundClass).style('fill', '');
        return this;
    };


    var _hoverItem = function(id, index) {
        svg.select(stackedbarPrefix +''+ id).selectAll('.'+backgroundClass).style('fill', 'url(#bar-shadow)')
        svg.select(stackedbarPrefix +''+ id).selectAll('.'+barClass)
            // .attr('transform', 'translate(0, 0.1)')
           // .style('filter', 'url(#drop-shadow)')
            .text(function(d){ return d.score });
        return this;
    };


    var _unhoverItem = function(id, index) {
        if(!_this.selectedItem) {
            svg.select(stackedbarPrefix +''+ id).selectAll('.'+backgroundClass).style('fill', '')
            svg.select(stackedbarPrefix +''+ id).selectAll('.'+barClass)
                // .attr('transform', 'translate(0, 0.2)')
                .style('filter', '')
                .text('');
        }
        return this;
    };


    var _clearEffects = function() {
        this.deselectAllItems();
        return this;
    };


    //  Redraw without animating when the container's size changes
    var _resize = function(containerHeight){
        if(this.isRankingDrawn) RANKING.Render.resizeCanvas(containerHeight);
        return this;
    };

    var _getHeight = function() {
        return $('.'+svgClass).height();
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    Ranking.prototype = {
        build: _build,
        update: _update,
        clear: _clear,
        reset: _reset,
        selectItem: _selectItem,
        deselectAllItems : _deSelectAllItems,
        hoverItem: _hoverItem,
        unhoverItem: _unhoverItem,
        highlightItems: _highlightItems,
        clearEffects: _clearEffects,
        resize: _resize,
        getHeight: _getHeight
    };

    return Ranking;
})();


module.exports = Ranking;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0), __webpack_require__(2)))

/***/ }),
/* 23 */,
/* 24 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 25 */,
/* 26 */,
/* 27 */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {
var Urank = __webpack_require__(7);


module.exports = (function(){

    var user_id = 2;

    var $message = $('.processing-message'),
        $numResultsMsg = $('.num-results-msg'),
        $bookmarks = $('.control-panel .container .bookmark-area'),
        $bookmarkTitle = $('.control-panel h4');

    var options = {
        elem : {
            tagCloudRoot: '#tagcloud',
            tagBoxRoot: '#tagbox',
            contentListRoot: '#contentlist',
            visCanvasRoot: '#viscanvas',
            neighborscloudRoot: '#neighborscloud'
        },
        dataAttr : {
            id : 'id',
            title : 'title',
            description : 'abstract',
            pretty_title: 'pretty_title',
            pretty_description: 'pretty_abstract',
            show :[
                { name: 'begintime', pretty: 'Date', type: 'date' },
                { name: 'video_url', pretty: 'Video URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'slide_url', pretty: 'Slides URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'paper_url', pretty: 'Paper URL', type: 'url', exclude_null : true, exlude_empty : true }
            ]
        },
        features:{
            neighbors: true
        },
        dataConnector : {
            urls: {
                get_data: '/comet_urank/get-colvideos/',
                get_keywords: '/comet_urank/get-keywords/',
                get_tags: '',
                get_usertags: '/comet_urank/get-usertags/'+user_id+'/',
                urank: '/comet_urank/urank_service/'
            }
        },
        keywordExtractor: {
            useLocal: false,
            minDocFrequency: 1,
            minRepetitionsInDocument: 1,
            maxKeywordDistance: 3,
            minRepetitionsProxKeywords: 2
        },
        rankingModel: {
            useLocal : false,
            rankBy: 'CB',
            rs : [
                {
                    name: 'CB',
                    active: true,
                    weight : 1.0,
                    attr : 'keywords',
                    pretty: 'Content Ranking'
                },
                {
                    name: 'CF',
                    active: false,
                    weight : 0,
                    attr : 'neighbors',
                    pretty: 'Social Ranking'
                }
            ]
        },
        tagCloud: {
            numCategories : 1
        },
        tagBox: {
            useHybridHeader: true
        },
        rankingRepresentation: {
            split_by: 'rs'                  // rs || feature
        },
        neighborscloud: {
            minFontSize : 8,               // in px    
            fontSizeGrowth: 0.02               // minFontSize + fontSizeGrowth * keyword.score (df)   
        },
    };

    var urank = new Urank(options);
    urank.load();
  
    

    // console.log(Test.sum());
    // console.log(Test.add1toa().sum());
    // console.log(Test.add1tob().sum());
    // console.log(Test.clear().sum());
    // console.log(Test);

})();

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),
/* 28 */,
/* 29 */,
/* 30 */,
/* 31 */,
/* 32 */,
/* 33 */,
/* 34 */,
/* 35 */,
/* 36 */,
/* 37 */,
/* 38 */,
/* 39 */,
/* 40 */,
/* 41 */
/***/ (function(module, exports, __webpack_require__) {

// JS
__webpack_require__(27);

// SCSS
__webpack_require__(24);
__webpack_require__(5);


/***/ })
],[41]);
//# sourceMappingURL=main_comet-7606bdd01eca464f9450.js.map

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

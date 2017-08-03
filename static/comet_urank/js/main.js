
var Urank = require('urank');


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

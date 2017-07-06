
// var Urank = require('../../../../plugins/urank');
var Urank = require('urank');

module.exports = (function(){

    var user_id = 2;
    // var actionLogger = new ActionLogger();

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
                { name: 'author_list', pretty: 'Authors', type: 'string', exclude_null : true, exlude_empty : true },
                { name: 'content_type', pretty: 'Type', type: 'string', exclude_null : true, exlude_empty : true }
            ]
        },
        features:{
            neighbors: true
        },
        dataConnector : {
            urls: {
                get_data: 'http://localhost:8000/cn_urank/get-talks/',
                get_keywords: 'http://localhost:8000/cn_urank/get-keywords/',
                get_neighbors: 'http://localhost:8000/cn_urank/get-neighbors/',
                urank: 'http://localhost:8000/cn_urank/urank_service/'
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
            useLocal : false
        },
        tagCloud: {
            numCategories : 1
        },
        tagBox: {
            useHybridHeader: true
        },
        rankingRepresentation: {
            split_by: 'rs'                  // rs || feature
        }
    };

    var urank = new Urank(options);
    urank.load();
  
    

    // console.log(Test.sum());
    // console.log(Test.add1toa().sum());
    // console.log(Test.add1tob().sum());
    // console.log(Test.clear().sum());
    // console.log(Test);

})();

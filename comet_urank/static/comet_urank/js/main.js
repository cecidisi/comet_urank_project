// import $ from 'jquery';
// import _ from 'underscore';
// import actionLogger from './ActionLogger';
// import Urank from '../../../../plugins/static/plugins/urank/js/controller/urank';

// let $ = require('jquery');
// let _ = require('underscore');
// let actionLogger = require('./ActionLogger');
// let Urank = require('../../../../plugins/static/plugins/urank/js/controller/urank');

console.log('jquery == ' + !!$);
console.log('underscore == ' + !!_);

(function(){

    var user_id = 2;
    var actionLogger = new ActionLogger();

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
            usertagBox: '#usertags'
        },
        dataAttr : {
            id : 'id',
            title : 'title',
            description : 'detail',
            show :[
                { name: 'begintime', pretty: 'Date', type: 'date' },
                { name: 'video_url', pretty: 'Video URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'slide_url', pretty: 'Slides URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'paper_url', pretty: 'Paper URL', type: 'url', exclude_null : true, exlude_empty : true }
            ]
        },
        dataConnector : {
            urls: {
                get_data: 'http://localhost:8000/comet_urank/get-colvideos/',
                get_keywords: 'http://localhost:8000/comet_urank/get-keywords/',
                get_tags: '',
                get_usertags: 'http://localhost:8000/comet_urank/get-usertags/'+user_id+'/',
                urank: 'http://localhost:8000/comet_urank/urank_service/'
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

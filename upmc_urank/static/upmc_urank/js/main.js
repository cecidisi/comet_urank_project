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

    // var _this = this;
    // this.data = [];

    // var dsm = new datasetManager();
    var actionLogger = new ActionLogger();

    var $message = $('.processing-message'),
        $numResultsMsg = $('.num-results-msg'),
        $bookmarks = $('.control-panel .container .bookmark-area'),
        $bookmarkTitle = $('.control-panel h4');

    // var urank = new Urank(options);

    $.get("http://ipinfo.io", function(response) {
        // actionLogger.log(actionLogger.action.ipLogged, response);
        console.log(response);
    }, "jsonp");

    //actionLogger.getActionCount();

    console.log('ENTRA A MAIN');


    ////////////////////////////////////////////////////////////////////////////
    var options = {
        elem : {
            tagCloudRoot: '#tagcloud',
            tagBoxRoot: '#tagbox',
            contentListRoot: '#contentlist',
            visCanvasRoot: '#viscanvas',
            usertagBox: '#usertags'
        },
        dataAttr : {
            id : 'col_id',
            title : 'title',
            description : 'detail',
            description_clean : 'detail_clean',
            show :[
                { name: 'begintime', pretty: 'Date', type: 'date' },
                { name: 'video_url', pretty: 'Video URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'slide_url', pretty: 'Slides URL', type: 'url', exclude_null : true, exlude_empty : true },
                { name: 'paper_url', pretty: 'Paper URL', type: 'url', exclude_null : true, exlude_empty : true }
            ]
        },
        keywordExtractor: {
            minDocFrequency: 1,
            minRepetitionsInDocument: 1,
            maxKeywordDistance: 3,
            minRepetitionsProxKeywords: 2
        }
    };

    var urank = new Urank(options);
    var urankFuncs = [
        function() {
            ServerConnector.getColloquia(1, function(data){
                console.log('Retrieved ' + data.length + ' documents');
                console.log(data[0]);
                urank.loadData(data);
            });
        },
        function() {
            console.log('RETRIEVE USERTAGS!!');
            ServerConnector.getUserTags(2, function(usertags){
                console.log('Retrieved ' + usertags.length  + ' usertags');
                urank.loadUserTags(usertags);
            });    
        }
        
    ];

    urankFuncs.forEach(function(func){
        func();
    });

    // ServerConnector.getColloquia(1, function(data) {
    //     console.log('Retrieved ' + data.length + ' documents');
    //     console.log(data[0]);
    //     urank.loadData(data);

    // })
    

    // console.log(Test.sum());
    // console.log(Test.add1toa().sum());
    // console.log(Test.add1tob().sum());
    // console.log(Test.clear().sum());
    // console.log(Test);

})();


var Urank = require('urank');
// var ActionLogger = require('./action-logger')

module.exports = (function(){
    var bookmarks = [];  // { id, pos, title }

    var $message = $('.processing-message'),
        $numResultsMsg = $('.num-results-msg'),
        $bookmarks = $('.control-panel .container .bookmark-area'),
        $bookmarkTitle = $('.control-panel h4'),
        $btnDone = $('#btn-done');

    $(function(){
    	var options = require('./urank_options');
	    var urank = new Urank(options);
	    urank.load();	
    })
    // $(document).ready(function(){
    // 	var options = require('./urank_options');
	   //  var urank = new Urank(options);
	   //  urank.load();	
    // })
    
})();

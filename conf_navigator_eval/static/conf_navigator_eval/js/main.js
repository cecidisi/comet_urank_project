
var Urank = require('urank');
var server = require('./server-connector');
var ActionLogger = require('./action-logger')

module.exports = (function(){
    var logger = new ActionLogger();
    var bookmarks = [];  // { id, pos, title }

    var $message = $('.processing-message'),
        $numResultsMsg = $('.num-results-msg'),
        $bookmarks = $('.control-panel .container .bookmark-area'),
        $bookmarkTitle = $('.control-panel h4'),
        $btnDone = $('#btn-done');

    var rs = $('#rs').text();
    var options = require('./urank_options')(rs);
    // console.log(urank_options);


    var callbacks = {
        // Click on item on list or ranking
        onItemClicked: function(obj){
            // { index , id, title }
            logger.log({
                'action': logger.action.documentClicked, 'pos': obj.index+1, 'id': obj.id, 'description': obj.title
            });
        },
        // Bookmark or unbookmark
        onFaviconClicked: function(obj) {
            // { index, id, title, state }
            var action;
            var pos = parseInt(obj.index + 1);
            if(obj.state === 'on') {
                bookmarks.push({ 'id': obj.id, 'pos': pos, 'title': obj.title });
                // assign action
                action = logger.action.documentBookmarked;
                // call server to bookmark in CN
                server.bookmarkCN(obj.id);
            } else {
                var idx = _.findIndex(bookmarks, function(bm){ return bm.id === obj.id });
                bookmarks.splice(idx, 1);
                // assign action
                action = logger.action.documentUnbookmarked;
                // call server to unbookmark in CN
                server.unbookmarkCN(obj.id);
            }
            console.log('Pos in main = ' + pos);
            // console.log(bookmarks);
            // log action
            logger.log({ 'action': action, 'pos': pos, 'id': obj.id, 'description': obj.title })
        },
        onRatingClicked: function(documentId, index, rating) {
            bookmarks[bookmarks.length - 1].rating = rating;
            console.log(bookmarks);
        },
        onTagSelected: function(tag){
            var action = logger.action.tagSelected;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'description': tag.type+'-'+tag.name }
            console.log(obj);
            logger.log(obj);
        },
        onTagWeightChanged: function(tag){
            var action = logger.action.tagWeightChanged;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'description': tag.type+'-'+tag.name+'-'+tag.weight }
            console.log(obj);
            logger.log(obj);
        },
        onTagDeleted: function(tag){
            var action = logger.action.tagDeleted;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'description': tag.type+'-'+tag.name }
            console.log(obj);
            logger.log(obj);
        }


    }
    options.callbacks = callbacks;
    console.log(options);
    var urank = new Urank(options);
    urank.load();
  

    $btnDone.click(function(evt){
        evt.stopPropagation();
        if(bookmarks.length < 2) {
            alert('Please bookmark at least 2 papers');
            return;
        }
        var logs = logger.getAllLogs();
        var elapsedTime = logger.getElapsedTime();
        server.submitTask({ 
            action_logs: logs,
            bookmarks: bookmarks,
            elapsed_time: elapsedTime
        });
    });


})();

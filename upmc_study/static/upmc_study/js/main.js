
var Urank = require('urank');
var server = require('./server-connector');
var ActionLogger = require('./action-logger')

module.exports = (function(){

    var $message = $('.processing-message'),
        $numResultsMsg = $('.num-results-msg'),
        $bookmarkTitle = $('.control-panel h4'),
        $btnLogs = $('#btn-logs'),
        $btnBookmarks = $('#btn-bookmarks'),
        $btnDone = $('#btn-done');

    var getCurrentUser = function(){
        return parseInt(sessionStorage['user_id'])
    }

    var logger = new ActionLogger()

    var callbacks = {
        // Bookmark or unbookmark
        onFaviconClicked: function(obj) {
            // { index, id, title, state }
            var action = obj.state === 'on' ? logger.action.documentBookmarked : logger.action.documentUnbookmarked;
            var pos = parseInt(obj.index + 1);
            var bm = {
                'user_id': getCurrentUser(),
                'item_id': obj.id,
                'item_title': obj.title,
                'pos': pos
            }
            
            if(obj.state === 'on') {
                // bookmarks.push({ 'id': obj.id, 'pos': pos, 'title': obj.title });
                server.bookmark(bm);
            } else {
                // var idx = _.findIndex(bookmarks, function(bm){ return bm.id === obj.id });
                // bookmarks.splice(idx, 1);
                server.unbookmark(bm);
            }
            console.log('Pos in main = ' + pos);
            logger.log({ 'action': action, 'pos': pos, 'id': obj.id, 'name': obj.title })
        },

        onTagSelected: function(tag){
            var action = logger.action.tagSelected;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'name': tag.name }
            logger.log(obj);
        },

        onTagWeightChanged: function(tag){
            var action = logger.action.tagWeightChanged;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'name': tag.name, 'value': tag.weight }
            logger.log(obj);
        },

        onTagDeleted: function(tag){
            var action = logger.action.tagDeleted;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'name': tag.name }
            logger.log(obj);
        },

        onFeatureSearched: function(tag){
            var action = logger.action.featureSearched;
            var obj = { 'action': action, 'pos': parseInt(tag.index)+1, 'id': tag.id, 'name': tag.name }
            logger.log(obj);
        },

        onFacetFiltered: function(facet){
            var action = logger.action.facetFiltered;
            var obj = { 'action': action, 'name': facet.type, 'value': facet.value } 
            logger.log(obj);
        },

        // Click on item on list or ranking
        onItemClicked: function(obj){
            // { index , id, title }
            logger.log({
                'action': logger.action.documentClicked, 'pos': obj.index+1, 'id': obj.id, 'name': obj.title
            });
            logger.openDocument({
                'item_id': obj.id, 'item_name': obj.title, 'pos': obj.index+1,
            });
        },

        onDocViewerHidden: function(){
            logger.closeDocument();
        },

        onReset: function() {
            logger.closeDocument();
        }

    };

    window.onload = function(){
        var options = require('../../../../upmc/static/upmc/js/urank_options');
        // Overwrite URLs related to ranking
        options.dataConnector.urls.update_ranking = 'update-ranking/';
        options.dataConnector.urls.urank = 'urank-service/';
        options.dataConnector.urls.filter_articles_by_year = 'filter-articles-by-year/[from_year]/[to_year]/';
        options.dataConnector.urls.get_document_details = 'get-article-details/[doc_id]/[decoration]/';
        options.dataConnector.urls.show_more_data = 'get-more-articles/[user_id]/[current_count]/'

        console.log(options)
        // Assign custom callbacks
        options.callbacks = callbacks;

        sessionStorage['user_id'] = $('#user_id').text();

        var urank = new Urank(options);
        urank.setUser(getCurrentUser());
        urank.load();
        logger.start()
    }
    
    $btnLogs.click(function(evt){
        evt.stopPropagation();
        var obj = {  
            'user_id': getCurrentUser(),
            'elapsed_time': logger.getElapsedTime(),
            'action_logs': logger.getActionLogs(), 
            'time_logs': logger.getTimeLogs() 
        }
        console.log(obj)
    });

    $btnDone.click(function(evt){
        evt.stopPropagation();
        server.submitTask({ 
            'user_id': getCurrentUser(),
            'elapsed_time': logger.getElapsedTime(),
            'action_logs': logger.getActionLogs(), 
            'time_logs': logger.getTimeLogs() 
        })
    })


    $btnBookmarks.click(function(evvt){
        evt.stopPropagation();
    })


})();

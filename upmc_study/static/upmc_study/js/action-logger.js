
var ActionLogger = (function(){

    var _this;
    var storageKey = 'urank-test';

    function ActionLogger(){
        _this = this;
        this.action = {
            // urank
            tagHovered: 'tag hovered',
            tagSelected: 'tag selected',
            tagDropped: 'tag dropped',
            tagWeightChanged: 'tag weight changed',
            tagDeleted: 'tag deleted',
            documentClicked: 'document clicked',
            documentBookmarked: 'document bookmarked',
            documentUnbookmarked: 'document unbookmarked',
            documentWatched: 'document watched',
            documentUnwatched: 'document unwatched',
            featureSearched: 'keyword searched',
            facetFiltered: 'facet filtered',
            reset: 'reset'
        };
        this.start();
    }

    ActionLogger.prototype = {
        
        start: function(){
            this.action_buffer = [];
            this.time_buffer = []
            this.curDoc = undefined;
            this.start_tmsp = Math.round($.now()/1000);
        },

        getCurrentTimestamp: function(){
            // in seconds
            return Math.round($.now()/1000 - this.start_tmsp)
        },

        action: function(){
            return this.action;
        },

        log: function(params) {
            var timestamp = this.getCurrentTimestamp()
            this.action_buffer.push({
                timestamp: timestamp,
                action: params.action,
                item_id: params.id || null,
                item_name: params.name || null,
                pos: params.pos || null,
                value: params.value || null
            });
            console.log("Logged " + params.action + ' (' + timestamp + ')');
        },

        openDocument: function(doc){
            this.curDoc = doc;
            this.curDoc.timestamp = this.getCurrentTimestamp();
        },

        closeDocument: function(){
            if(this.curDoc) {
                this.curDoc.duration = this.getCurrentTimestamp() - this.curDoc.timestamp;
                this.time_buffer.push(this.curDoc);
                this.curDoc = undefined;
            }
        },
 
        getActionLogs: function(){
            return this.action_buffer;
        },

        getTimeLogs: function(){
            return this.time_buffer;
        },

        getElapsedTime: function() {
            return this.getCurrentTimestamp();
        }
    };
    return ActionLogger;
})();

module.exports = ActionLogger;

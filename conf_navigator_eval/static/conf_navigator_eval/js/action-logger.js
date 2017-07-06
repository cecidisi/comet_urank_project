
var ActionLogger = (function(){

    var _this;
    var storageKey = 'urank-test';

    function ActionLogger(){
        _this = this;
        this.action = {
            // urank
            tagHovered: 'tag hovered',
            tagClicked: 'tag clicked',
            tagDropped: 'tag dropped',
            tagWeightChanged: 'tag weight changed',
            tagDeleted: 'tag deleted',
            documentClicked: 'document clicked',
            documentBookmarked: 'document bookmarked',
            documentUnbookmarked: 'document unbookmarked',
            documentWatched: 'document watched',
            documentUnwatched: 'document unwatched',
            frequencyChanged: 'frequency range changed',
            wordSearched: 'keyword searched',
            reset: 'reset'
        };
        this.buffer = [];
        this.start_tmsp = $.now();
    }


    ActionLogger.prototype = {
        action: function(){
            return this.action;
        },

        log: function(params) {
            var timestamp = $.now() - this.start_tmsp;
            this.buffer.push({
                timestamp: timestamp,
                action: params.action,
                pos: params.pos || -1,
                id: params.id || -1,
                description: params.description || ''
            });
            console.log("Logged " + params.action + ' (' + timestamp + ')');
        },
 
        getAllLogs: function(){
            return this.buffer;
        },

        getElapsedTime: function() {
            return $.now() - this.start_tmsp;
        }
    };
    return ActionLogger;
})();

module.exports = ActionLogger;

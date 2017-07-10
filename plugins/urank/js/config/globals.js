'use strict';
var Globals  = {
    STR : {
        NO_VIS : "No visualization yet!",
        DROPPED : "Dropped!",
        DROP_TAGS_HERE : "Drop tags here!",
        JUST_RANKED : "new",
        SEARCHING : "Searching..."//,
        // UNDEFINED : 'undefined'
    },

    RANKING_STATUS : {
        new : 'new',
        update : 'update',
        unchanged : 'unchanged',
        no_ranking : 'no_ranking'
    },

    USER_ACTION : {
        added: 'keyword added',
        deleted: 'keyword deleted',
        weighted: 'changed weight',
        bookmarked: 'document bookmarked',
        unbookmarked: 'document unbookmarked',
        watched: 'watching document',
        unwatched: 'document unwatched',
        mode: 'ranking mode changed'
    },

    LEGENDS: {
        rating: 'How would you rate this item?'
    }
};

module.exports = Globals;
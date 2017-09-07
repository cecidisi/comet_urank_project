var TagCloudDefault = require('../views/tagcloud/tagCloudDefault');
var Ranking = require('../views/viscanvas/ranking');

var VIEWS = {
    VISCANVAS : {
        ranking: Ranking
        // detailedView: DetailedView
    },
    TAGCLOUD : {
        default: TagCloudDefault
    //    ,landscape: LandscapeTagCloud
    }    
};


module.exports = VIEWS;
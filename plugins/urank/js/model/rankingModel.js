var Globals = require('../config/globals');
var RSContent = require('./RSContent');


var RankingModel = (function() {
    'use strict';


    var _this;
    function RankingModel(config, dataConn){
        this.conf = config;
        this.dataConn = dataConn || null;
        this.clear();
        _this = this;
    }


    /*******************************************
    * Functions
    *******************************************/
    var assignRankingPositionsAndShift = function(_data, _score){
        var currentScore = Number.MAX_VALUE;
        var currentPos = 1;
        var itemsInCurrentPos = 0;
        _data.forEach(function(d, i){
            if(d.ranking[_score] > 0){
                if( d.ranking[_score] < currentScore ){
                    currentPos = currentPos + itemsInCurrentPos;
                    currentScore = d.ranking[_score];
                    itemsInCurrentPos = 1;
                } else{
                    itemsInCurrentPos++;
                }
                d.ranking.pos = currentPos;
            } else{
                d.ranking.pos = 0;
            }
            // shift computation
            d.ranking.posChanged = d.ranking.prev_pos > 0 ? d.ranking.prev_pos - d.ranking.pos : 1000;
        });
        return _data;
    };


    /**
     *	Creates the ranking items with default values and calculates the weighted score for each selected keyword (tags in tag box)
     * */
     // FIX!!!!!!!!!!
    var updateRanking =  function(oldRanking, query, rs_conf){
        var cbWeight = rs_conf.CB.weight; // (score == RANKING_MODE.overall.attr) ? opt.rWeight : 1;
        var tuWeight = rs_conf.TU.weight; // (score == RANKING_MODE.overall.attr) ? (1- opt.rWeight) : 1;
        var score =  rs_conf[rs_conf.rankBy].name;
        var newRanking = oldRanking.slice();
        // MAKE ONE LOOP
        newRanking.forEach(function(d){ d.ranking.prev_pos = d.ranking.pos; });
        if(cbWeight)            
            newRanking = RSContent.getCBScores({ data: newRanking, keywords: opt.query, options: { rWeight: cbWeight } });
        // if(tuWeight)
        //     ranking = _this.tuRS.getTagUserScores({ user: opt.user, keywords: opt.query, data: ranking, options: { rWeight: tuWeight } });
        newRanking.forEach(function(d){
            d.ranking.total_score = 0;
            if(cbWeight)
                d.ranking.total_score += d.ranking.cb_score;
            // if(tuWeight)
            //     d.ranking.total_score += d.ranking.tu_score;
        });

        var secScore = undefined;
        if(score === 'CB' && tuWeight) secScore = rs_conf.TU.name;
        if(score === 'TU' && cbWeight) secScore = rs_conf.CB.name;
        newRanking = newRanking.sort(function(d1, d2){
            if(d1.ranking[score] > d2.ranking[score]) return -1;
            if(d1.ranking[score] < d2.ranking[score]) return 1;
            if(d1.ranking[secScore] && d1.ranking[secScore] > d2.ranking[secScore]) return -1;
            if(d1.ranking[secScore] && d1.ranking[secScore] < d2.ranking[secScore]) return 1;
            return 0;
        });
        newRanking = assignRankingPositionsAndShift(newRanking, score);
        return newRanking;
    };



    var updateStatus =  function(ranking, curStatus) {

        // if(_this.ranking.length === 0)
        //     return Globals.RANKING_STATUS.no_ranking;

        // if(_this.status === Globals.RANKING_STATUS.no_ranking)
        //     return Globals.RANKING_STATUS.new;

        // for(var i in _this.ranking) {
        //     if(_this.ranking[i].ranking.posChanged > 0)
        //         return Globals.RANKING_STATUS.update;
        // }
        if(ranking.length === 0)
            return Globals.RANKING_STATUS.no_ranking;

        if(curStatus === Globals.RANKING_STATUS.no_ranking)
            return Globals.RANKING_STATUS.new;

        for(var i in ranking) {
            if(ranking[i].ranking.pos_changed > 0)
                return Globals.RANKING_STATUS.update;
        }
        return Globals.RANKING_STATUS.unchanged;
    };



    var _setData = function(data) {
        if(this.useLocal) {
            this.status = Globals.RANKING_STATUS.no_ranking;
            this.data = data.slice() || [];
            this.ranking = this.data.slice();
            this.ranking.forEach(function(d){
                d.ranking = {
                    pos: 0,
                    pos_changed: 0,
                    prev_pos: 0,
                    total_core: 0,
                    cb_score: 0,
                    cb_max_score: 0,
                    cb_details: [],
                    tu_score: 0,
                    tu_details: {}
                };
            });
        }
        return this;
    };



    var _update = function(params, onDone) {
        // CONF
        // rs : [
        //     {
        //         name: 'CB',
        //         active: true,
        //         weight : 0.5,
        //         attr : 'keywords'
        //     },
        //     {
        //         name: 'CF',
        //         active: true,
        //         weight : 0.5,
        //         attr : 'neighbors'
        //     }
        // ],
        // rankBy : 'CB'

        // this.query = params.query;
        this.features = params.features;
        this.conf = params.rs_conf;
        this.rankBy = this.conf.rankBy;

        var onRankingUpdated = function(ranking) {
            _this.ranking = ranking;
            _this.status = updateStatus(ranking, _this.status);
            // onDone(this.ranking, _this.status);
            onDone(_this.ranking, _this.status);
        };

        if(this.conf.useLocal) {
            // sync
            // var ranking = this.query.length ? updateRanking(this.ranking, params) : [];
            var ranking = this.features.keywords.length ? updateRanking(this.ranking, params) : [];
            onRankingUpdated(ranking);
        } else { 
            // async
            _this.dataConn.updateRanking(params, function(ranking) {
                onRankingUpdated(ranking);
            });    
        }
    };


    var _reset = function() {
        this.previousRanking = [];
        this.ranking = [];
        this.status = updateStatus();
        this.query = [];
        return this;
    };



    var _clear = function() {        
        this.ranking = [];
        this.data = [];
        this.query = [];
        this.status = Globals.RANKING_STATUS.no_ranking;
        // if(!this.useLocal)
        //     this.dataConn.clearRanking();
        return this;
    };




/****************************************************************************************************
 *
 *   RankingModel Prototype
 *
 ****************************************************************************************************/
    RankingModel.prototype = {
    //return {

        setData: _setData,

        update: _update,

        reset: _reset,

        clear: _clear,

        getRanking: function() {
            // return this.ranking;
            return this.ranking;
        },

        getStatus: function() {
            // return this.status;
            return this.status;
        },

        getOriginalData: function() {
            // return this.data;
            return this.data;
        },

        getQuery: function() {
            // return this.query;
            return this.query;
        },

        getRankingDict: function(){
            var dict = {};
            // this.ranking.forEach(function(d){ dict[d.id] = d; });
            this.ranking.forEach(function(d){ dict[d.id] = d; });
            return dict;
        },

        getMaxTagFrequency: function(){
            return this.tuRS.getmaxSingleTagFrequency();
        },

        getActualIndex: function(index){
            // if(this.status == Globals.RANKING_STATUS.no_ranking)
            //     return index;
            // return this.ranking[index].originalIndex;
            if(this.status == Globals.RANKING_STATUS.no_ranking)
                return index;
            return this.ranking[index].originalIndex;
        },
        getDocumentById: function(id) {
            var getId = function(d){ return d.id === id };
            // return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[_.findIndex(this.data, getId)] : this.ranking[_.findIndex(this.ranking, getId)];
            return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[_.findIndex(this.data, getId)] : this.ranking[_.findIndex(this.ranking, getId)];
        },
        getDocumentByIndex: function(index) {
            // return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[index] : this.ranking[index];
            return this.status === Globals.RANKING_STATUS.no_ranking ? this.data[index] : this.ranking[index];
        }
    };

    return RankingModel;
})();


module.exports = RankingModel;


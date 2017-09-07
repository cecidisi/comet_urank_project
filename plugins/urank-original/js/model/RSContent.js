
var RSContent = (function(){
    'use strict';

    // function RSContent() {}

    var getEuclidenNorm = function(docKeywords) {
        var acumSquares = 0;
        Object.keys(docKeywords).forEach(function(k){
            acumSquares += docKeywords[k] * docKeywords[k];
        });
        return Math.sqrt(acumSquares);
    };


    return {
        getCBScores : function(options) {
            var opt = $.extend(true, {
                data: [],
                keywords: [],
                options: {
                    rWeight: 1
                }
            }, options);
            var _data = opt.data.slice();

            if(opt.keywords.length > 0) {
                _data.forEach(function(d, i) {
                    d.ranking.cb_score = 0;
                    d.ranking.cb_max_score = 0;
                    d.ranking.cb_details = [];
                    var docNorm = getEuclidenNorm(d.keywords);
                    var unitQueryVectorDot = parseFloat(1.00/Math.sqrt(opt.keywords.length));
                    var max = 0;
                    opt.keywords.forEach(function(q) {
                    // termScore = tf-idf(d, t) * unitQueryVector(t) * weight(query term) / |d|   ---    |d| = euclidenNormalization(d)
                        var termScore = (d.keywords[q.stem]) ? ((parseFloat(d.keywords[q.stem]) / docNorm) * unitQueryVectorDot * parseFloat(q.weight * opt.options.rWeight)).round(3) :  0;
                        // if item doesn't contain query term => maxScore and overallScore are not changed
                        d.ranking.cb_score += termScore;
                        d.ranking.cb_max_score = termScore > d.ranking.cb_max_score ? termScore : d.ranking.cb_max_score;
                        d.ranking.cb_details.push({ term: q.term, stem: q.stem, weightedScore: termScore });
                    });
                });
            }
            return _data;
        }
    }
})();

module.exports = RSContent;



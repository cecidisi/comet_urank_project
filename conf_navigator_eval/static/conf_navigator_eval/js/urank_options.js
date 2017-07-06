var default_options = {
    elem : {
        tagBoxRoot: '#tagbox',
        contentListRoot: '#contentlist',
        visCanvasRoot: '#viscanvas',
        tagCloudRoot: '#tagcloud',
        neighborscloudRoot: '#neighborscloud'
    },
    dataAttr : {
        id : 'id',
        title : 'title',
        description : 'abstract',
        pretty_title: 'pretty_title',
        pretty_description: 'pretty_abstract',
        show :[
            { name: 'author_list', pretty: 'Authors', type: 'string', exclude_null : true, exlude_empty : true },
            { name: 'content_type', pretty: 'Type', type: 'string', exclude_null : true, exlude_empty : true }
        ]
    },
    features:{
        neighbors: true
    },
    dataConnector : {
        urls: {
            get_data: 'http://localhost:8000/cn_urank/get-talks/',
            get_keywords: 'http://localhost:8000/cn_urank/get-keywords/',
            get_neighbors: 'http://localhost:8000/cn_urank/get-neighbors/',
            urank: 'http://localhost:8000/cn_urank/urank_service/'
        }
    },
    keywordExtractor: {
        useLocal: false,
        minDocFrequency: 1,
        minRepetitionsInDocument: 1,
        maxKeywordDistance: 3,
        minRepetitionsProxKeywords: 2
    },
    rankingModel: {
        useLocal : false
    },
    tagCloud: {
        numCategories : 1
    },
    tagBox: {

    },
    rankingRepresentation: {
        split_by: 'rs'                  // rs || feature
    }
};

var rs_options = {
    'CB': {
        elem: {
            neighborscloudRoot: ''      // disable neighbors cluoud
        },
        features: {
            keywords: true,
            neighbors: false
        },
        rankingModel: {
            rankBy: 'CB',
            rs : [
                {
                    name: 'CB',
                    active: true,
                    weight : 1.0,
                    attr : 'keywords',
                    pretty: 'Content Ranking'
                },
                {
                    name: 'CF',
                    active: false,
                    weight : 0,
                    attr : 'neighbors',
                    pretty: 'Social Ranking'
                }
            ]
        }
    },
    'SF': {
        elem: {
            tagCloudRoot: ''            // disable tagcloud
        },
        features: {
            keywords: false,
            neighbors: true
        },
        rankingModel: {
            rankBy: 'CF',
            rs : [
                {
                    name: 'CB',
                    active: false,
                    weight : 0,
                    attr : 'keywords',
                    pretty: 'Content Ranking'
                },
                {
                    name: 'CF',
                    active: true,
                    weight : 1.0,
                    attr : 'neighbors',
                    pretty: 'Social Ranking'
                }
            ]
        }
    },
    'CB_SF': {
        features: {
            keywords: true,
            neighbors: true
        },
        rankingModel: {
            rankBy: 'CB',
            rs : [
                {
                    name: 'CB',
                    active: true,
                    weight : 0.5,
                    attr : 'keywords',
                    pretty: 'Content Ranking'
                },
                {
                    name: 'CF',
                    active: true,
                    weight : 0.5,
                    attr : 'neighbors',
                    pretty: 'Social Ranking'
                }
            ]
        },
        tagBox: {
            header: {
                enabled: true,
                useHybrid: false,
                useSplit: true
            }
        }
    },
    'HYB': {
        rankingModel: {
            rankBy: 'overall',
            rs : [
                {
                    name: 'CB',
                    active: true,
                    weight : 0.5,
                    attr : 'keywords',
                    pretty: 'Content Ranking'
                },
                {
                    name: 'CF',
                    active: true,
                    weight : 0.5,
                    attr : 'neighbors',
                    pretty: 'Social Ranking'
                }
            ]
        },
        tagBox: {
            header: {
                enabled: true,
                useHybrid: true,
                useSplit: false
            }
        }
    }
};

var get_options = function(rs) {
    console.log('Send options for ' + rs);
    var opt = $.extend(true, {}, default_options, rs_options[rs]);
    return opt;
}

module.exports = get_options;
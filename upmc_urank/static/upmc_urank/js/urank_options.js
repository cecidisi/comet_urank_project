var default_options = {
    elem : {
        tagBoxRoot: '#tagbox',
        contentListRoot: '#contentlist',
        visCanvasRoot: '#viscanvas',
        tagCloudRoot: '#tagcloud'
    },
    dataAttr : {
        id : 'id',
        title : 'title',
        description : 'abstract',
        pretty_title: 'pretty_title',
        pretty_description: 'pretty_abstract',
        show :[
            { name: 'pub_type', label: 'Publication Type', type: 'string', exclude_null: true, exlude_empty : true }
            // { name: 'author_list', pretty: 'Authors', type: 'string', exclude_null : true, exlude_empty : true },
            // { name: 'content_type', pretty: 'Type', type: 'string', exclude_null : true, exlude_empty : true }
        ]
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
    },
    dataConnector : {
        urls: {
            get_data: '/upmc_urank/get-articles/',
            get_keywords: '/upmc_urank/get-keywords/',
            urank: '/upmc_urank/urank_service/'
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
    tagCloud : {        
        numCategories : 1,
        minFontSize : 11,               // in px    
        fontSizeGrowth: 0.02           // minFontSize + fontSizeGrowth * keyword.score (df) 
    },
    tagBox: {

    },
    docViewer: {
        attrToShow: [{
            attr: 'pub_type', label: 'Publication Type'
        }] 
    },
    rankingRepresentation: {
        split_by: 'feature'                  // rs || feature
    }
};


module.exports = default_options;
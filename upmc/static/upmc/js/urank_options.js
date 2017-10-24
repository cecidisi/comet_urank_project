var default_options = {
    elem : {
        tagBoxRoot: '#tagbox',
        contentListRoot: '#contentlist',
        visCanvasRoot: '#viscanvas',
        tagCloudRoot: '#tagcloud',
        searchInputRoot: '#search-features'
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
        useLocal : false,
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
            get_data: 'get-articles/',
            get_keywords: 'get-keywords/',
            get_keyphrases: 'get-keyphrases/[kw_id]',
            get_document_details: 'get-article-details/[doc_id]/[decoration]',
            update_ranking: 'update-ranking/',
            urank: 'urank_service/',
            search_features: 'search-features/[feature_type]/[text]'
        }
    },
    keywordExtractor: {
        useLocal: false,
        minDocFrequency: 1,
        minRepetitionsInDocument: 1,
        maxKeywordDistance: 3,
        minRepetitionsProxKeywords: 2
    },
    tagCloud : {        
        numCategories : 1,
        minFontSize : 11,               // in px    
        fontSizeGrowth: 0.02           // minFontSize + fontSizeGrowth * keyword.score (df) 
    },
    tagBox: {

    },
    searchInput: {
        type: 'keyword'
    },
    docViewer: {
        attrToShow: [{
            attr: 'authors_list', label: 'Authors'
        }, {
            attr: 'pub_details.year', label: 'Year'
        }, {
            attr: 'pub_type', label: 'Publication Type'
        }] 
    },
    rankingRepresentation: {
        split_by: 'feature'                  // rs || feature
    }
};


module.exports = default_options;
var default_options = {
    elem : {
        tagBoxRoot: '#tagbox',
        contentListRoot: '#contentlist',
        visCanvasRoot: '#viscanvas',
        tagCloudRoot: '#tagcloud',
        searchInputRoot: '#search-features',
        rangeFilterRoot: '#timeslider'
    },

    dataConnector : {
        urls: {
            get_data: '/urank/upmc/get-articles/',
            get_keywords: '/urank/upmc/get-keywords/',
            get_document_details: '/urank/upmc/get-article-details/[doc_id]/[decoration]/',
            get_facets: '/urank/upmc/get-facets/[facet_type]/',
            get_keyphrases: '/urank/upmc/get-keyphrases/[kw_id]/',
            search_features: '/urank/upmc/search-features/[feature_type]/[text]/',            
            update_ranking: '/urank/upmc/update-ranking/',
            urank: '/urank/upmc/urank-service/',
            filter_articles_by_year: '/urank/upmc/filter-articles-by-year/[from_year]/[to_year]/',
            show_more_data: '/urank/upmc/get-more-articles/[current_count]/'
        },
        path_to: {
            results: 'results',
            count: 'count'
        }
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
    facets: [ 
        {
            name: 'Year',
            type: 'year'
        }
    ],
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
    keywordExtractor: {
        useLocal: false,
        minDocFrequency: 1,
        minRepetitionsInDocument: 1,
        maxKeywordDistance: 3,
        minRepetitionsProxKeywords: 2
    },
    tagCloud : {        
        numCategories : 1,
        minFontSize : 9,               // in px    
        fontSizeGrowth: 0.009,           // minFontSize + fontSizeGrowth * keyword.score (df) 
        maxFontSize: 23
    },
    tagBox: {

    },
    searchInput: {
        type: 'keyword'
    },
    contentList: {
        showWatchIcon: false
    },
    docViewer: {
        useLocal: false,
        attrToShow: [{
            attr: 'authors_list', label: 'Authors'
        }, {
            attr: 'year', label: 'Year'
        }, {
            attr: 'pub_type', label: 'Publication Type'
        }] 
    },
    rankingRepresentation: {
        split_by: 'feature'                  // rs || feature
    }
};


module.exports = default_options;
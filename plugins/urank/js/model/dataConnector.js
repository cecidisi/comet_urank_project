
DataConnector = (function(){
	var _this;

	function DataConnector(options){
		this.urls = options.urls;
		_this = this;
	}

	var sendRequest = function(options, onDone, onFail){
		var request_options = $.extend(true, {
			'url' : '',
			'type': 'GET'
		}, options);
		onDone = onDone || function(data){};
		onFail = onFail || function(){};
		if(!request_options.url || request_options.url === '') return { 'message': 'No URL set' };
		var timelapse = $.now()
		$.ajax(request_options)
		.fail(function(jqXHR, textStatus){
	        console.log('DataConnector ERROR ' + request_options.type + ' ' + request_options.url);
	        // console.log(jqXHR)
	        onFail();
	    }).done(function(resp) {
	        timelapse = $.now() - timelapse
	        console.log('DataConnector: successful request ' + request_options.type + ' ' + request_options.url + ' (' + timelapse + ' ms)');
        	console.log(resp.results.length);    
	        onDone(resp.results);
	    });

	};

	var getData = function(onDone) {
		sendRequest({ url: _this.urls.get_data }, onDone);
	};

	var getKeywords = function(onDone) {
		sendRequest({ url: _this.urls.get_keywords }, onDone);
	};

	var getTags = function(onDone){
		sendRequest({ url: _this.urls.get_tags }), onDone;
	};

	var getUsertags = function(onDone){
		sendRequest({ url: _this.urls.get_usertags }, onDone);
	};

	var getNeighbors = function(onDone){
		sendRequest({ url: _this.urls.get_neighbors }, onDone);
	};

	var postUrank = function(url, data, onDone){
		console.log('DataConnector: Start request --> ' + data.operation);
		sendRequest({ 
			'type': 'POST',
			'url': url, 
			'data':  JSON.stringify(data),
			'contentType': 'application/json; charset=utf-8'
		}, onDone);
	}

	var updateRanking = function(params, onDone) {
		var url = this.urls.urank || this.urls.update_ranking;
		var data = $.extend(true, { 'operation': 'update' }, params);
		postUrank(url, data, onDone);
	};

	var clearRanking = function(onDone) {
		var url = this.urls.urank || this.urls.clear_ranking;
		var data = { 'operation': 'clear' };
		postUrank(url, data, onDone);
	};

	var showMoreRanking = function(onDone){
		var url = this.urls.urank || this.urls.show_more_ranking;
		var data = { 'operation': 'show_more' };
		postUrank(url, done, onDone);
	};

	var getDocumentDetails = function(params, onDone){
		var url = this.urls.urank || this.urls.get_document_details;
		var data = $.extend(true, { 'operation': 'get_document_details' }, params);
		postUrank(url, data, onDone);
	};


	DataConnector.prototype = {
		getData: getData,
		getKeywords: getKeywords,
		getTags: getTags,
		getUsertags: getUsertags,
		getNeighbors: getNeighbors,
		updateRanking: updateRanking,
		clearRanking, clearRanking,
		showMoreRanking : showMoreRanking,
		getDocumentDetails: getDocumentDetails
	};

	return DataConnector;

})()


module.exports = DataConnector;
var ServerConnector = (function(){
	var host = '/urank/upmc-study/';

	var sendRrequest = function(options, cb){
		$.ajax(options)
		.fail(function(jqXHR, textStatus){
	        console.log(textStatus);
	    }).done(function(resp) {
	        console.log('ServerConnector: successful request');
	        console.log(resp);
	        if(cb) cb(resp.results);
	    });
	};

	var bookmark = function(params, onDone){
		sendRrequest({
			type: 'POST',
			url: host + 'bookmark/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, onDone);
	};

	var unbookmark = function(params, onDone){
		sendRrequest({
			type: 'POST',
			url: host + 'unbookmark/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, onDone);
	};

	var getBookmarks = function(onDone){
		sendRrequest({
			type: 'GET',
			url: host + 'get-bookmarks/' + getCurrentUser() + '/',
		}, onDone)
	};

	var submitTask = function(params){
		sendRrequest({
			type: 'POST',
			url: host + 'submit-task/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, function(){
			console.log(sessionStorage['user_id'])
			url = host + 'review/[user_id]/'
			console.log(host)
			window.location = url.replace('[user_id]', sessionStorage['user_id'])
		})
	};

	var getCurrentUser = function(){
        return sessionStorage['user_id']
    }


	var finishReview = function(){
		window.location = host + 'questionnaire/'
	};


	var submitTaskPubmed = function(params){
		sendRrequest({
			type: 'POST',
			url: host + 'pubmed-submit-task/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, function(){
			console.log(sessionStorage['user_id'])
			window.location = url = host + 'pubmed-questionnaire/';
		})

	}

	return {
		bookmark: bookmark,
		unbookmark: unbookmark,
		getBookmarks: getBookmarks,
		submitTask: submitTask,
		finishReview: finishReview,
		submitTaskPubmed: submitTaskPubmed
	}

})();

module.exports = ServerConnector;
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

	var bookmark = function(params){
		sendRrequest({
			type: 'POST',
			url: host + 'bookmark/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, function(){
			console.log('Bookmarked paper #' + params.item_title)
		})
	};

	var unbookmark = function(article_id){
		sendRrequest({
			type: 'POST',
			url: host + 'unbookmark/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, function(){
			console.log('Bookmarked paper #' + params.item_title)
		})
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

	return {
		bookmark: bookmark,
		unbookmark: unbookmark,
		submitTask: submitTask,
		finishReview: finishReview
	}

})();

module.exports = ServerConnector;
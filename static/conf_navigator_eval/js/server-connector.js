var ServerConnector = (function(){
	var host = '/urank/cn_urank_eval';

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

	var startFirstTask = function(){
		window.location = host + '/set-task/';
	};


	var submitTask = function(params){
		sendRrequest({
			type: 'POST',
			url: host + '/submit-task/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'
		}, function(){
			window.location = host + '/questions/'
		})
	};

	var submitQuestions = function(params){
		sendRrequest({
			type: 'POST',
			url: host + '/submit-questions/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'			
		}, function(){
			window.location = host + '/set-task/'
		});
	};

	var submitFinalSurvey = function(params){
		sendRrequest({
			type: 'POST',
			url: host + '/submit-final-survey/',
			data: JSON.stringify(params),
			contentType: '"application/x-www-form-urlencoded"'			
		}, function(){
			window.location = host + '/finish-task/'
		});
	}

	var bookmarkCN = function(content_id){
		sendRrequest({
			url: host + '/bookmark-cn/' + content_id
		}, function(){
			console.log('Bookmarked paper #' + content_id + ' in CN')
		})
	};

	var unbookmarkCN = function(content_id){
		sendRrequest({
			url: host + '/unbookmark-cn/' + content_id
		}, function(){
			console.log('Unbookmarked paper #' + content_id + ' in CN')
		})
	}

	return {
		startFirstTask: startFirstTask,
		submitTask: submitTask,
		submitQuestions: submitQuestions,
		submitFinalSurvey: submitFinalSurvey,
		bookmarkCN: bookmarkCN,
		unbookmarkCN: unbookmarkCN
	}

})();

module.exports = ServerConnector;
var ServerConnector = (function(){
	var host = '/cn_urank_eval';

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

	return {
		startFirstTask: startFirstTask,
		submitTask: submitTask,
		submitQuestions: submitQuestions,
		submitFinalSurvey: submitFinalSurvey
	}

})();

module.exports = ServerConnector;
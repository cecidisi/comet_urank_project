var server = require('./server-connector');
var ActionLogger = require('./action-logger')


module.exports = (function(){
	var logger = new ActionLogger();
	var $btnDone = $('#btn-done-pubmed-task');

    var getCurrentUser = function(){
        return parseInt(sessionStorage['user_id'])
    }

	$btnDone.click(function(evt){
		evt.stopPropagation();
		server.submitTaskPubmed({ 
			'user_id': getCurrentUser(),
			'elapsed_time': logger.getElapsedTime()
		});
	})

	window.onload = function(){
		logger.start()
		sessionStorage['user_id'] = $('#user_id').text();
	}



})()
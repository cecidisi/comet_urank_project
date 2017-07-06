var server = require('./server-connector')


module.exports = (function($) {

	$('#btn-done').click(function(evt){
		evt.stopPropagation();
		server.submitQuestions({}, function(){
			console.log('Submitted questions')
		})

	});






})(jQuery)
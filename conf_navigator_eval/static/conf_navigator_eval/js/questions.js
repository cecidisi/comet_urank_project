var server = require('./server-connector')


module.exports = (function($) {

	$('#btn-done').click(function(evt){
		evt.stopPropagation();
		var values = [];
		var goodToSubmit = true;
		$('.question-item').each(function(idx){			
			var value = $(this).find('.active').find('input[type="radio"]').val();
			if(value)
				values.push(value);
			else
				goodToSubmit = false;

		})
		console.log(goodToSubmit);
		if(goodToSubmit){
			server.submitQuestions({ 'values': values }, function(){
				console.log('Submitted questions')
			})	
		} else{
			alert('Please answer all questions');
		}
		

	});






})(jQuery)
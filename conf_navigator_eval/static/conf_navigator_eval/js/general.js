var server = require('./server-connector')


module.exports = (function($) {

	// Done Intro w/ Task Description
	$('#btn-done-intro').click(function(evt){
		evt.stopPropagation();
		server.startFirstTask();
	})


	// Done Task Questions
	$('#btn-done-questions').click(function(evt){
		evt.stopPropagation();
		var values = [];
		var goodToSubmit = true;
		$('.question-item').each(function(idx){			
			var qid = parseInt($(this).attr('qid'));
			var value = parseInt($(this).find('.active').find('input[type="radio"]').val());
			if(value)
				values.push({ qid: qid, val: value });
			else
				goodToSubmit = false;

		})
		console.log(values)
		if(goodToSubmit){
			server.submitQuestions({ 'values': values }, function(){
				console.log('Submitted questions')
			})	
		} else{
			alert('Please answer all questions');
		}
	});

	// Done Final Survey
	$('#btn-done-final').click(function(evt){
		evt.stopPropagation();
		var values = [];
		var goodToSubmit = true;
		$('.radio-btn-group').each(function(idx){						
			var qid = parseInt($(this).attr('qid'));
			var value = $(this).find('input[type="radio"]:checked').val();
			if(value)
				values.push({ qid: qid, val: value });
			else
				goodToSubmit = false;
		})
		console.log(values)
		if(goodToSubmit){
			console.log('Ready to submit')
			server.submitFinalSurvey({ 'values': values }, function(){
				console.log('Submitted Final Survey')
			})	
		} else{
			alert('Please answer all questions');
		}

	})



})(jQuery)
webpackJsonp([3],{

/***/ 25:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 26:
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function($) {var ServerConnector = (function(){
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
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),

/***/ 29:
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(jQuery) {var server = __webpack_require__(26)


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
/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(0)))

/***/ }),

/***/ 36:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 40:
/***/ (function(module, exports, __webpack_require__) {

// JS
__webpack_require__(29);

// SCSS
__webpack_require__(25);
__webpack_require__(36);


/***/ })

},[40]);
//# sourceMappingURL=conf_nav_eval_general-7606bdd01eca464f9450.js.map
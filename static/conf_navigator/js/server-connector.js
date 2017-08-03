var ServerConnector = (function(){
	// var host = 'http://localhost:8000/comet_urank/';
	var host = '/comet_urank/';
	var cur_col_page = 1;

	var sendRrequest = function(options){

		var opt = $.extend(true, {
			url : '',
			method: 'GET',
			onFail : function(){},
			onDone : function(data){}
		}, options);

		$.ajax({
	        url : host + '' + opt.url,
	        method : opt.method
	    }).fail(function(jqXHR, textStatus){
	        console.log(textStatus);
	        opt.onFail();
	    }).done(function(resp) {
	        console.log('ServerConnector: successful request');
	        opt.onDone(resp.results);
	    });

	};

// 'http://localhost:8000/comet_urank/colloquia-with-video/?format=json'
	var getColloquia = function(page, onDone){
		cur_col_page = page ? cur_col_page : 1;
		var url = 'colvideos/?format=json&page=' + cur_col_page 
		sendRrequest({
			url : url,
			onDone : onDone
		})
	};

	var getMoreColloquia = function(onDone) {
		getColloquia(onDone, ++cur_col_page);
	};


	var getUserTags = function(user_id, onDone){
		sendRrequest({
			url : 'usertags/' + user_id+ '/?format=json',
			onDone : onDone
		});
	};

	var getColloquiaAndUserTags = function(user_id) {
		getColloquia(null, null, function(_data) {
			getUserTags(user_id, function(_usertags) {
				onDone(_data, _usertags);
			});
		});

	};

	return {
		getColloquia : getColloquia,
		getUserTags : getUserTags,
		getColloquiaAndUserTags : getColloquiaAndUserTags
	}

})();
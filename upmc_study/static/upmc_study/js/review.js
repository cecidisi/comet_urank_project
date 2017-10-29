var server = require('./server-connector')


module.exports = (function($) {

	$('#btn-download').find('a').attr('href', '/urank/upmc-study/download-bookmarks/'+sessionStorage['user_id'])

	$('#btn-done-review').click(function(evt){
		evt.stopPropagation();
		server.finishReview();
	});

})(jQuery)
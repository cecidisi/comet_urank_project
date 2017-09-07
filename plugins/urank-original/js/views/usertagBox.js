var UsertagBox = (function(){

	var _this, $root, $usertagbox;
	var usertags, s;

	function UsertagBox(params){
		_this = this;
	    s = $.extend({
	        root: '',
	        attr: {},
	        options: {},
	        cb:{
	            onUsertagMouseEnter: function(index, id){},
	            onUsertagMouseLeave: function(index, id){},
	            onUsertagClick: function(index, id){},
	            onUsertagSelected: function(index, id){}
	        }
	    }, params);
	    this.usertags = [];

	   	$root = $(s.root);
	}

	var build = function(usertags, colors){
		this.usertags = usertags;

		$root.attr('class', 'urank-usertagbox');
		$usertagbox = $('<div/>', { class: 'urank-usertagbox-inner' }).appendTo($root);

		this.usertags.forEach(function(t, index) {
			var $tag = $('<div/>', {
				id: 'urank-usertag-' + t.id,
				'utag-id': t.id,
				'utag-pos': index,
				'class': 'urank-usertag',
				'name': t.tag,
				'html': t.tag
			}).appendTo($usertagbox);
			// Bind event handlers and set style
			$tag.off()
				.on({
					'click': function(evt){
						s.cb.onUsertagSelected(index, t.id);
					},
					'mouseenter': function(evt){
						s.cb.onUsertagMouseEnter(index, t.id)
					},
					'mouseleave': function(evt){
						s.cb.onUsertagMouseLeave(index, t.id)
					}
				})
				.css({
					'color': colors(t.tag),
					'font-size': (s.options.minFontSize + t.count * s.options.fontSizeGrowth)+'px'	
				});

		});
	};


	var selectUsertag = function(index, id, color) {
		var $tag = $('#urank-usertag-' + id);
		var $clone = $tag.clone().attr('id', 'urank-usertag-'+id+'-clon');
		$tag.after($clone);
		$tag.addClass('selected').css({
			'color': 'white',
			'background': color
		});
	};


	var onUsertagMouseEntered = function(index, id){
		var $tag = $('#urank-usertag-' + id);
		if(!$tag.hasClass('selected'))
			$tag.addClass('hovered');
	};

	var onUsertagMouseLeft = function(index, id){
		var $tag = $('#urank-usertag-' + id);
		$tag.removeClass('hovered');
	};


	

	UsertagBox.prototype = {
		build : build,
		selectUsertag: selectUsertag,
		onUsertagMouseEnter: onUsertagMouseEntered,
		onUsertagMouseLeave: onUsertagMouseLeft
	};

	return UsertagBox;
})()

module.exports = UsertagBox;
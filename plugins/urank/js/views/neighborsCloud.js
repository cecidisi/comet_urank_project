var NeighborsCloud = (function(){

	var _this, $root, $neighborcloud;
	var s;

	function NeighborsCloud(params){
		_this = this;
	    s = $.extend({
	        root: '',
	        attr: {},
	        options: {},
	        cb:{
	            onNeighborTagMouseEnter: function(index, id){},
	            onNeighborTagMouseLeave: function(index, id){},
	            onNeighborTagClick: function(index, id){},
	            onNeighborTagSelected: function(index, id){}
	        }
	    }, params);
	    this.neighbors = [];

	   	$root = $(s.root);
	}

	var build = function(neighbors, colors){
		this.neighbors = neighbors;

		$root.addClass('urank-tag-container');
		$neighborcloud = $('<div/>', { class: 'urank-tag-container-inner' }).appendTo($root);

		this.neighbors.forEach(function(t, index) {
			var $tag = $('<div/>', {
				id: 'urank-neighbortag-' + t.neighbor.id,
				// 'vtag-id': t.neighbor.id,
				// 'vtag-pos': index,
				'class': 'urank-tag',
				'name': t.tag,
				'html': t.neighbor.name
			}).appendTo($neighborcloud);
			// Bind event handlers and set style
			$tag.off()
				.on({
					'click': function(evt){
						var tid = '#urank-neighbortag-' + t.neighbor.id;
						var $tag = $(tid)
						if(!$tag.hasClass('selected')) {
							s.cb.onNeighborTagSelected(index, t.neighbor.id);	
						}
					},
					'mouseenter': function(evt){
						s.cb.onNeighborTagMouseEnter(index, t.neighbor.id)
					},
					'mouseleave': function(evt){
						s.cb.onNeighborTagMouseLeave(index, t.neighbor.id)
					}
				})
				.css({
					'color': colors(t.neighbor.name),
					'font-size': (s.options.minFontSize + t.score * s.options.fontSizeGrowth)+'px'	
				});

		});
	};


	var selectNeighborTag = function(index, id, color) {
		var $tag = $('#urank-neighbortag-' + id);
		if(!$tag.hasClass('selected')) {
			var $clone = $tag.clone().attr('id', 'urank-neighbortag-'+id+'-clon');
			$tag.after($clone);
			$tag.addClass('selected').css({
				'color': 'white',
				'background': color
			});
		}
	};


	var onNeighborTagMouseEntered = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		if(!$tag.hasClass('selected'))
			$tag.addClass('hovered');
	};

	var onNeighborTagMouseLeft = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		$tag.removeClass('hovered');
	};


	

	NeighborsCloud.prototype = {
		build : build,
		selectNeighborTag: selectNeighborTag,
		onNeighborTagMouseEnter: onNeighborTagMouseEntered,
		onNeighborTagMouseLeave: onNeighborTagMouseLeft
	};

	return NeighborsCloud;
})()

module.exports = NeighborsCloud;
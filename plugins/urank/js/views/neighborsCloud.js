var NeighborsCloud = (function(){

	var _this, $root, $neighborcloud, $tooltip;
	var s;
	var simFeat = {
			'C': 'Co-authorship', 
			'G': 'Geographic Distance', 
			'I': 'Similar Interests', 
			'P': 'Publication Similarity', 
			'S': 'Social Context'
		};

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

	var setTagProperties = function($tag, t, index) {
		$tag.off().on({
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
				'color': _this.colors(t.neighbor.name),
				'font-size': (s.options.minFontSize + t.score * s.options.fontSizeGrowth)+'px',
				'background': ''
			});

	}

	var addTooltip = function(tag, $tag){
		$('.tag-tooltip').remove();
		$tooltip = $('<div/>', { id: 'neighbor-tag-tooltip', class: 'tag-tooltip' }).appendTo($root);
	
		var $titleWrapper = $('<div/>', { class: 'title-wrapper' }).appendTo($tooltip);
		$('<div/>', { class: 'title', html: tag.neighbor.name }).appendTo($titleWrapper);
		$('<div/>', { class: 'friend' }).appendTo($tooltip);

		if(tag.explanations.friend)
			var $feat = $('<div/>', { class: 'sim-feature' }).appendTo($tooltip);
			$('<span/>', { name: 'friend', html: 'Friend' }).appendTo($feat)
				.css('font-size', '18px');
		for(feat in simFeat){
			if(simFeat[feat]) {
				var $feat = $('<div/>', { class: 'sim-feature' }).appendTo($tooltip);
				var fontSize = Math.min(6 + tag.explanations[feat] * 8, 20);
				$('<span/>', { name: feat, html: simFeat[feat] }).appendTo($feat)
					.css('font-size', fontSize+'px');	
			}
			
		}

		var height = $tooltip.height();
		var width = $tooltip.width();
		var top = parseInt($tag.offset().top) - height+50;
		var left = parseInt($neighborcloud.offset().left) - width;
		$tooltip.css({ top: top, left: left, width: width });

	};

	var build = function(neighbors, colors){
		this.neighbors = neighbors;
		this.colors = colors;

		$root.addClass('urank-tag-container');
		$container = $('<div/>', { class: 'urank-tag-container-outer'}).appendTo($root);
		$('<div/>', { class: 'urank-hidden-scrollbar' }).appendTo($container)
		$scrollable = $('<div/>').appendTo($container).addClass('urank-hidden-scrollbar-inner')
            // .on('scroll', onRootScrolled);
        $neighborcloud = $('<div/>').appendTo($scrollable).addClass('urank-tag-container-inner');
		// $neighborcloud = $('<div/>', { class: 'urank-tag-container-inner' }).appendTo($scrollable);
		// addTooltip();

		this.neighbors.forEach(function(t, index) {
			var $tag = $('<div/>', {
				id: 'urank-neighbortag-' + t.neighbor.id,
				'class': 'urank-tag',
				'name': t.tag,
				'html': t.neighbor.name
			}).appendTo($neighborcloud);
			// Bind event handlers and set style
			setTagProperties($tag, t, index);
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

	var tooltipTimeout, fadeOutTimeOut;

	var onNeighborTagMouseEntered = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		if(!$tag.hasClass('selected'))
			$tag.addClass('hovered');

		// fill tooltip
		tooltipTimeout = setTimeout(function(){
			var tag = _this.neighbors[index];
			addTooltip(tag, $tag);
			
			$tooltip.fadeIn();
			fadeOutTimeOut = setTimeout(function(){
			    $tooltip.fadeOut();
			}, 4000);
		}, 100);
		
	};


	var onNeighborTagMouseLeft = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);
		$tag.removeClass('hovered');
		clearTimeout(tooltipTimeout);
        clearTimeout(fadeOutTimeOut);
        if($tooltip)
        	$tooltip.hide();
	};


	var restoreTag = function(index, id){
		var $tag = $('#urank-neighbortag-' + id);		            // is in tagcloud
		var $clonedTag = $('#urank-neighbortag-' + id + '-clon');   // is in tagbox, will be deleted sync
		var $dummyTag = $clonedTag.clone();                     	// need dummy for animation, clone is removed
		$dummyTag.attr('id', 'dummy-tag-' + id);
		console.log('Animating ' + $dummyTag.attr('id'));
		//  Save offset in tagBox before detaching
		var oldOffset = $clonedTag.offset();
		var newOffset = $tag.offset();
		// Detach tag from tag cloud, attach temporarily to body and place it in old position (in tagBox)
		$dummyTag.appendTo('body')
		    .css({ position: 'absolute', top: oldOffset.top, left: oldOffset.left, 'z-index': 9999 });
		// Animate tag moving from tag box to tag cloud
		$dummyTag.animate({ top: newOffset.top, left: newOffset.left }, 800, 'swing', function() {
		    //  Detach from body after motion animation is complete and append to tag container again
		    $dummyTag.remove();
		    $tag.removeClass().addClass('urank-tag'); //.setTagStyle();
		    setTagProperties($tag, _this.neighbors[index], index);
		    // $tag = $tag.detach();
		    // $clonedTag.after($tag);
		    // $clonedTag.remove();
		    // $tag.css({ position: '', top: '', left: '', 'z-index': '' }).setTagStyle();
		    // setTagProperties($tag);
		});

	}

	

	NeighborsCloud.prototype = {
		// init
		build : build,
		// when user selects a tag, node, ot person icon
		selectNeighborTag: selectNeighborTag,
		// mouse over
		onNeighborTagMouseEnter: onNeighborTagMouseEntered,
		// mouse leave
		onNeighborTagMouseLeave: onNeighborTagMouseLeft,
		// when tag deleted in tagbox (box above ranking)
		restoreTag: restoreTag
	};

	return NeighborsCloud;
})()

module.exports = NeighborsCloud;

(function($) {

    $.fn.extend({
        pin: function(args) {

            var options = $.extend({
                top: 0,
                left: 0,
                bottom: 0,                  // only if relativeTo != 'none'
                right: 0,                   // only if relativeTo != 'none'
                container: 'window',
                relativeTo: 'parent'        // parent | none | custom selector
            }, args);

            return this.each(function() {
                var $this = $(this);
                if($this.css('visibility') == 'visible') {

                    if(options.relativeTo !== 'none') {
                        var $parent = options.relativeTo == 'parent' ? $this.parent() : options.relativeTo;
                        options.left = options.right ? options.left + $parent.fullOffset().left + $parent.fullWidth() + options.right : options.left + $parent.fullOffset().left;
                        options.top = options.bottom ? options.top + $parent.fullOffset().top + $parent.fullHeight() + options.bottom : options.top + $parent.fullOffset().top;
                    }

                    $this.css({ position: 'fixed', top: options.top, left: options.left, 'z-index': 9999 });

                    if(options.container !== 'window') {
                        var $container = $(options.container),
                            containerOffset = $container.offset(),
                            containerHeight = $container.height(),
                            //     containerWidth = $container.width(),
                            thisOffset = $this.fullOffset(),
                            thisHeight = $this.height();
                        //   thisWidth = $this.width();

                        if(thisOffset.top < containerOffset.top || (thisOffset.top + thisHeight) > (containerOffset.top + containerHeight)
                           /*|| thisOffset.left < containerOffset.left || (thisOffset.left + thisWidth) > containerOffset.left + containerWidth */)
                            $this.css('visibility', 'hidden');
                    }
                }
                return $this;
            });
        },
        
        fullHeight: function() {
            var m = {
                border: {
                    top: $(this).css('border-top-width') || '0px',
                    bottom: $(this).css('border-bottom-width') || '0px'
                },
                padding: {
                    top: $(this).css('padding-top') || '0px',
                    bottom: $(this).css('padding-bottom') || '0px'
                }
            };

            return $(this).height()
                + parseInt(m.border.top.replace('px', ''))
                + parseInt(m.padding.top.replace('px', ''))
                + parseInt(m.border.bottom.replace('px', ''))
                + parseInt(m.padding.bottom.replace('px', ''));
        },

        fullOffset: function() {
            return {
                top: $(this).offset().top + parseInt($(this).css('margin-top').replace('px', '')),
                    //  parseInt($(this).css('border-top-width').replace('px', '')) +
                    //parseInt($(this).css('padding-top').replace('px', '')) +
                left: $(this).offset().left + parseInt($(this).css('margin-left').replace('px', ''))
                    //parseInt($(this).css('border-left-width').replace('px', '')) +
                    //parseInt($(this).css('padding-left').replace('px', ''))
            };
        },

        fullWidth: function() {
            return $(this).width()
                + parseInt($(this).css('border-left-width').replace('px', ''))
                + parseInt($(this).css('padding-left').replace('px', ''))
                + parseInt($(this).css('border-right-width').replace('px', ''))
                + parseInt($(this).css('padding-right').replace('px', ''));
        },

        getText: function() {
            return $(this).clone().children().remove().end().text();
        },

        outerHTML: function() {
            return $(this).clone().wrap('<div></div>').parent().html();
        },

        scrollTo: function(target, options, callback){

            if(typeof options == 'function' && arguments.length == 2){
                callback = options;
                options = target;
            }

            var settings =
                $.extend({
                    scrollTarget  : target,
                    offsetTop     : 0,
                    duration      : 500,
                    easing        : 'swing'
                }, options);

            return this.each(function(){
                var scrollPane = $(this);

                var scrollTarget;
                if( typeof settings.scrollTarget == "number" ){
                    scrollTarget = settings.scrollTarget;
                }
                else{
                    if( settings.scrollTarget == "top" ){
                        scrollTarget = 0;
                    }
                    else{
                        scrollTarget = $(settings.scrollTarget);
                        settings.offsetTop += scrollPane.offset().top;
                    }
                }

                //var scrollTarget = (typeof settings.scrollTarget == "number") ? settings.scrollTarget : $(settings.scrollTarget);
                var scrollY = (typeof scrollTarget == "number") ? scrollTarget : scrollPane.scrollTop() + scrollTarget.offset().top - settings.offsetTop;

                scrollPane.animate({scrollTop : scrollY }, parseInt(settings.duration), settings.easing, function(){
                    if (typeof callback == 'function') { callback.call(this); }
                });
            });
        },

        // unfinished
        tooltip: function(options) {

            var tooltipClass = 'urank-tooltip';

            var $this = $(this);


            if(typeof options == 'string' && options == 'destroy'){


            } else if(typeof options == 'object') {
                var s = $.extend({
                    title: null,
                    message: '',
                    position: 'right',      //  right | left | top | bottom
                    type: 'default',        //  default | info |
                    root: 'body'
                }, options);

                $tooltip = $('<div></div>', { class: tooltipClass }).appendTo($this);

            }

            return $this;
        }

    });
    
    
}(jQuery));

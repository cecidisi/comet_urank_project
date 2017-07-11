
var Globals = require('../../config/globals');

var Ranking = (function(){

    var RANKING = {};
    var s, _this;
    var width, height, margin;
    var x, y, color, xAxis, yAxis, xUpperLimit;
    var svg;
    var data;
    var $root = $('');

    //  Classes
    var svgClass = 'urank-ranking-svg',
        axisClass = 'urank-ranking-axis',
        xClass = 'urank-ranking-x',
        xAxisLabelClass = 'urank-ranking-label',
        yClass = 'urank-ranking-y',
        stackedbarClass = 'urank-ranking-stackedbar',
        backgroundClass = 'urank-ranking-background',
        lightBackgroundClass = 'urank-ranking-light-background',
        darkBackgroundClass = 'urank-ranking-dark-background',
        selectedClass = 'selected',
        dimmedClass = 'dimmed',
        barClass = 'urank-ranking-bar',
        tuSectionClass = 'urank-tag-user-section';

    // Id
    var stackedbarPrefix = '#urank-ranking-stackedbar-';

    function Ranking(params) {
        _this = this;
        s = $.extend({
            root: '.urank-viscanvas-container',
            attr : {},
            options : {
                aes: {
                    lightBackgroundColor: '',
                    darkBackgroundColor: ''
                }
            },
            cb : {
                onItemClicked: function(doc, i){},
                onItemMouseEnter: function(doc, i){},
                onItemMouseLeave: function(doc, i){}
            }
        }, params);
        this.isRankingDrawn = false;
        this.selectedItem = null;
    }

    RANKING.Settings = {
        getExtendedData: function(params){
            var ranking = params.ranking.slice();
            var features = params.features;
            var conf = params.conf;
            var rankBy = params.conf.rankBy;
            var a = [];
            var colors = {};
            // Get tag name -> color mapping
            for(var fkey in features) {
                features[fkey].forEach(function(tag){
                    colors[tag.name] = tag.color;
                })
            }

            ranking.forEach(function(d, i) {
                d.bars = [];
                var x0 = 0.0;
                conf.rs.forEach(function(rs, j) {
                    if(rs.active) {
                        var RS = rs.name;
                        // x0 = rankBy === 'overall' ? x0 : j;
                        d.ranking[RS].details.forEach(function(item) {
                            var x1 = x0 + item.score; 
                            d.bars.push({
                                desc: item.name,
                                x0: x0,
                                x1: x1,
                                color: colors[item.name]
                            });
                            x0 = x1;
                        });
                        // update baseline x0 for next RS
                        x0 = rankBy === 'overall' ? x0 : j+1;
                    }
                });
                a.push(d);
            });
            return a;
        },
        getXUpperLimit: function(conf) {
            if(conf.rankBy === 'overall')
                return 1.0;
            var x_limit = conf.rs.filter(function(rs){ return rs.active }).length;
            return x_limit;
        }
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    RANKING.Evt = {};


    RANKING.Evt.itemClicked = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemClicked.call(this, d[s.attr.id], i);
    };

    RANKING.Evt.itemMouseEntered = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemMouseEnter.call(this, d[s.attr.id], i);
    };

    RANKING.Evt.itemMouseLeft = function(d, i){
        d3.event.stopPropagation();
        s.cb.onItemMouseLeave.call(this, d[s.attr.id], i);
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    RANKING.Render = {

        /******************************************************************************************************************
        *
        *	Draw ranking at first instance
        *
        * ***************************************************************************************************************/
        drawNew: function(data, containerHeight){
            margin = { top: 0, bottom: 0, left: 0, right: 0 };
            width = $root.width() - margin.left - margin.right;
            height = containerHeight;
            xUpperLimit = 1;

            // Define scales
            x = d3.scale.linear()
                .domain([0, xUpperLimit])
                .rangeRound( [0, width] );

            y = d3.scale.ordinal()
                .domain(data.map(function(d){ return d[s.attr.id]; }))
                .rangeBands( [0, height]);

            // Define axis' function
            xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .tickValues('');

            yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickValues("");

            // Draw chart main components
            //// Add svg main components
            svg = d3.select(s.root).append("svg")
                .attr("class", svgClass)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("width", width)
                .attr("height", height)
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("g")
                .attr("class", xClass + ' ' + axisClass)
                .attr("transform", "translate(0," + (height) + ")")
                .call(xAxis)
                .selectAll('text');

            svg.append("g")
                .attr("class", yClass +' '+axisClass)
                .call(yAxis)
                .selectAll("text");

            var stackedBars = svg.selectAll('.'+stackedbarClass)
            .data(data).enter()
            .append("g")
            .attr("class", stackedbarClass)
            .attr("id", function(d){ return "urank-ranking-stackedbar-" + d[s.attr.id]; })
            .attr( "transform", function(d) {return "translate(0, " + y(d[s.attr.id]) + ")"; })
            .on('click', RANKING.Evt.itemClicked)
            .on('mouseover', RANKING.Evt.itemMouseEntered)
            .on('mouseout', RANKING.Evt.itemMouseLeft);

            stackedBars.append('rect')
                .attr('class', function(d, i){ return (i%2) ? backgroundClass+' '+darkBackgroundClass : backgroundClass+' '+lightBackgroundClass; })
                .attr('x', 0)
                .attr('width', width)
                .attr('height', y.rangeBand())
                .style('fill', function(d, i){
                if(s.options.aes.lightBackgroundColor != '' && s.options.aes.darkBackgroundColor != '') {
                    if(i%2) return s.options.aes.darkBackgroundColor;
                    return s.options.aes.lightBackgroundColor;
                }
                return  '';
            });
            return this;
        },

        /******************************************************************************************************************
        *
        *	Redraw updated ranking and animate with transitions to depict changes
        *
        * ***************************************************************************************************************/
        redrawUpdated: function(params){
            data = RANKING.Settings.getExtendedData(params);   //(params.ranking, ranking_conf, params.colorScale);
//            width = $root.width();
            RANKING.Render.updateCanvasDimensions(params.listHeight);

            // Redefine x & y scales' domain
            d3.select(s.root).select('.'+svgClass).attr("width", width)
            svg.attr("width", width);

            // xUpperLimit =  data[0].ranking.total_score * 2.0;
            xUpperLimit =  RANKING.Settings.getXUpperLimit(params.conf);
            x.rangeRound( [0, width] ).domain([0, xUpperLimit]).copy();

//            y.rangeBands( [0, height], .02);
            y.rangeBands( [0, height]);
            y.domain(data.map(function(d){ return d[s.attr.id] })).copy();

            var transition = svg.transition().duration(750);
            var delay = function(d, i) { return i * 50; };

            transition.select('.'+xClass+'.'+axisClass).call(xAxis)
                .selectAll("g").delay(delay);

            transition.select('.'+yClass+'.'+axisClass).call(yAxis)
                .selectAll("g").delay(delay);

            RANKING.Render.drawStackedBars();

            ////////////////////////////////////////
            // CHECK IF THIS NEEDS TO BE ENABLED!!
            ////////////////////////////////////////
            // if(opt.ranking.social)
            //     RANKING.Render.drawTagsAndUsersHints(rankingModel.getQuery(), rankingModel.getMaxTagFrequency());

            return this;
        },



        /******************************************************************************************************************
        *
        *	Draw stacked bars either on draw or update methods. Animate with width transition
        *
        * ***************************************************************************************************************/
        drawStackedBars: function(){
            svg.selectAll('.'+stackedbarClass).data([]).exit();
            svg.selectAll('.'+stackedbarClass).remove();
            //svg.selectAll('.'+stackedbarClass).data(data).enter();

            setTimeout(function(){

                var stackedBars = svg.selectAll('.'+stackedbarClass)
                    .data(data).enter()
                    .append("g")
                    .attr("class", stackedbarClass)
                    .attr("id", function(d){ return "urank-ranking-stackedbar-" + d[s.attr.id]; })
                    .attr( "transform", function(d) {return "translate(0, " + y(d[s.attr.id]) + ")"; })
                    .on('click', RANKING.Evt.itemClicked)
                    .on('mouseover', RANKING.Evt.itemMouseEntered)
                    .on('mouseout', RANKING.Evt.itemMouseLeft);

                stackedBars.append('rect')
                    .attr('class', function(d, i){ return (i%2) ? backgroundClass+' '+darkBackgroundClass : backgroundClass+' '+lightBackgroundClass; })
                    .attr('x', 0)
                    .attr('width', width)
                    .attr('height', y.rangeBand())
                    .style('fill', function(d, i){
                        if(s.options.aes.lightBackgroundColor != '' && s.options.aes.darkBackgroundColor != '') {
                            if(i%2) return s.options.aes.darkBackgroundColor;
                            return s.options.aes.lightBackgroundColor;
                        }
                        return  '';
                    });

                stackedBars.selectAll('.'+barClass)
                    .data(function(d) { return d.bars })
                    .enter()
                    .append("rect")
                    .attr("class", barClass)
                    .attr("height", y.rangeBand())
                    .attr("x", function(d) { return x(d.x0); })
                    .attr("width", 0)
                    .attr('transform', 'translate(0, 0.2)')
                    .style("fill", function(d) { return d.color; });

                var bars = stackedBars.selectAll('.'+barClass);

                var getBarWidth = function(d) {
                    var barWidth = x(d.x1) - x(d.x0) - 0.2;
                    return barWidth > 0 ? barWidth : 0;    
                }
                
                var t0 = bars.transition()
                    .duration(800)
                    .attr({ 'width': function(d) { return getBarWidth(d) } });

            }, 800);
            return this;
        },

        /******************************************************************************************************************
        *
        *	Draw minimal views for tag- and user-based recommendations
        *
        * ***************************************************************************************************************/
        drawTagsAndUsersHints: function(query, maxTagFreq) {

            setTimeout(function(){

                var tagHintWidth = query.length * 6 + 6;
                var userHintWidth = 24;
                var xTagHintOffset = x(xUpperLimit) - tagHintWidth - userHintWidth;
                var xUserHintOffset = x(xUpperLimit) - userHintWidth;
                var maxBarHeight = y.rangeBand();

                // Define scales
                var xTU = d3.scale.ordinal().domain(query.map(function(q){ return q.stem; })).rangeBands( [0, tagHintWidth-6], .2);
                var yTU = d3.scale.linear().domain([0, maxTagFreq]).rangeRound([maxBarHeight, 0]);

                // Define axis' function
                var xAxisTU = d3.svg.axis().scale(xTU).orient("bottom").tickValues('');
                var yAxisTU = d3.svg.axis().scale(yTU).orient("left").tickValues('');

                var stackedbars = svg.selectAll('.'+stackedbarClass);

                var tagHints = stackedbars.append('g')
                    .attr('width', tagHintWidth)
                    .attr('height', maxBarHeight)
                    .attr("transform", function(d, i){ "translate(" + xTagHintOffset + "," + y(i) + ")" });

                // draw x axis
                tagHints.append('g')
                    .attr('class', xClass + ' ' + axisClass)
                    .attr('width', xTU.rangeBand())
                    .attr('transform', function(d, i){ return 'translate(' + xTagHintOffset + ',' + maxBarHeight + ')' })
                    .call(xAxisTU)
                    .selectAll('text');

                // draw y axis
                tagHints.append('g')
                    .attr('class', yClass + ' ' + axisClass)
                    .attr('height', maxBarHeight)
                    .attr('transform', function(d, i){ return 'translate(' + xTagHintOffset + ',0)' })
                    .call(yAxisTU)
                    .selectAll('text');

                // draw vertical tag bars
                tagHints.selectAll('.tag-bar')
                    .data(function(d) { return d.tags })
                    .enter()
                    .append("rect")
                    .attr("class", 'tag-bar')
                    .attr("x", function(t) { return xTagHintOffset + xTU(t.stem); })
                    .attr("width", xTU.rangeBand())
                    .attr("y", function(t) { return yTU(t.tagged); })
                    .attr("height", function(t){ return maxBarHeight - yTU(t.tagged); })
                    .style("fill", function(t) { return t.color; });

                // draw user hint
                var userHints = stackedbars.append('g')
                    .attr('class', 'urank-ranking-user-hint')
                    .attr('transform', function(d, i){ 'translate(' + xUserHintOffset + ',' + y(i) + ')' });

                userHints.append('svg:image')
                    .attr('xlink:href', function(d){ return d.ranking.tuMisc.users > 0 ? '../media/user.png' : '' })
                    .attr('x', xUserHintOffset)
                    .attr('width', 13)
                    .attr('y', 12)
                    .attr('height', 13)

                userHints.append('text')
                    .attr('dx', xUserHintOffset + 9)
                    .attr('dy', 15)
                    .text(function(d){ return d.ranking.tuMisc.users > 0 ? d.ranking.tuMisc.users : '' });

            }, 801);

            return this;
        },

        /******************************************************************************************************************
        *
        *	Create drop shadow for click effect on bars
        *
        * ***************************************************************************************************************/
        createShadow: function(){
            // filters go in defs element
            var defs = svg.append("defs");
            // create filter with id #drop-shadow
            // height=130% so that the shadow is not clipped
            var filter = defs.append("filter")
            .attr("id", "drop-shadow")
            .attr("height", "130%");
            // SourceAlpha refers to opacity of graphic that this filter will be applied to
            // convolve that with a Gaussian with standard deviation 3 and store result
            // in blur
            filter.append("feGaussianBlur")
                .attr("in", "SourceAlpha")
                .attr("stdDeviation", 2)
                .attr("result", "blur");
            // translate output of Gaussian blur to the right and downwards with 2px
            // store result in offsetBlur
            filter.append("feOffset")
                .attr("in", "blur")
                .attr("dx", 0)
                .attr("dy", 2)
                .attr("result", "offsetBlur");
            // overlay original SourceGraphic over translated blurred opacity by using
            // feMerge filter. Order of specifying inputs is important!
            var feMerge = filter.append("feMerge");
            feMerge.append("feMergeNode").attr("in", "offsetBlur")
            feMerge.append("feMergeNode").attr("in", "SourceGraphic");
            return this;
        },

        /******************************************************************************************************************
        *
        *	Create drop shadow for click effect on bars
        *
        * ***************************************************************************************************************/
        createBarHoverGradient: function(){
            var defs = svg.append("defs");
            var linearGradient = defs.append('linearGradient').attr('id', 'bar-shadow').attr('x1', '0%').attr('y1', '0%').attr('x2', '0%').attr('y2', '100%');
            // linearGradient.append('stop').attr('offset', '25%').style('stop-color', 'rgba(150,150,150,0.3)');
            // linearGradient.append('stop').attr('offset', '75%').style('stop-color', 'rgba(150,150,150,0.6)');
            // linearGradient.append('stop').attr('offset', '100%').style('stop-color', 'rgba(150,150,150,0.3)');
            linearGradient.append('stop').attr('offset', '100%').style('stop-color', 'rgba(200,200,200,1)');
            return this;
        },

        /*****************************************************************************************************************
        *
        *	Adjust height of svg and other elements when the ranking changes
        *
        * ***************************************************************************************************************/
        updateCanvasDimensions: function(listHeight){
            height = listHeight;
            y.rangeBands(height, .01);

            d3.select(svg.node().parentNode)    // var svg = svg > g
                .attr('height', height + margin.top + margin.bottom);

            svg.attr("height", height + 30)
                .attr("transform", "translate(" + (margin.left) + ", 0)");

            // update axes
            svg.select('.'+xClass+'.'+axisClass).attr("transform", "translate(0," + (height) + ")").call(xAxis.orient('bottom'));
            return this;
        },

        /*****************************************************************************************************************
        *
        *	Redraw without animating when the container's size changes
        *
        * ***************************************************************************************************************/
        resizeCanvas: function(containerHeight) {

            //  Resize container if containerHeight is specified
            if(containerHeight)
                $root.css('height', containerHeight);

            //  Recalculate width
            width = $root.width() - margin.left - margin.right;

            x.rangeRound([0, width]);
            y.rangeBands(height, .02);

            d3.select(svg.node().parentNode).attr('width', width + margin.left + margin.right);
            svg.attr("width", width);

            svg.selectAll('.' + darkBackgroundClass)
                .attr('width', width)
            svg.selectAll('.' + lightBackgroundClass)
                .attr('width', width)

            // update x-axis
            svg.select('.'+xClass + '.'+axisClass).call(xAxis.orient('bottom'));

            // Update bars
            svg.selectAll('.'+stackedbarClass).attr('width', width);
            svg.selectAll('rect.'+backgroundClass).attr('width', width);

            svg.selectAll('.'+barClass)
                .attr("x", function(d) { return x(d.x0); })
                .attr("width", function(d) { return x(d.x1) - x(d.x0); });
            return this;
        }
    };

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  Prototype methods

    var _build = function(data, containerHeight) {
        $root = $(s.root);
        _this.originalData = data;
        _this.originalHeight = containerHeight;
        RANKING.Render.drawNew(data, containerHeight).createBarHoverGradient();
        return this;
    }


    var _update = function(params){
        var updateFunc = {};
        updateFunc[Globals.RANKING_STATUS.new] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.update] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.unchanged] = RANKING.Render.redrawUpdated;
        updateFunc[Globals.RANKING_STATUS.no_ranking] = _this.reset;
        updateFunc[params.status].call(this, params);
        return this;
    };

    var _clear = function(){
        this.isRankingDrawn = false;
        $root.empty();
        return this;
    };


    var _reset = function() {
        _this.clear();
        _this.build(_this.originalData, _this.originalHeight);
        return this;
    };

    var _selectItem = function(id, index){
        _this.selectedItem = id;
        svg.selectAll('.'+stackedbarClass).style('opacity', 0.2);
        svg.select(stackedbarPrefix + '' + id).style('opacity', 1).select('.'+backgroundClass).style('fill', 'rgba(150,150,150,.5)');
        return this;
    };

    var _highlightItems = function(ids) {
        svg.selectAll('.'+stackedbarClass).style('opacity', function(d){ return (ids.indexOf(d[s.attr.id]) > -1) ? 1 : 0.2 });
        return this;
    };


    var _deSelectAllItems = function(){
        _this.selectedItem = undefined;
        svg.selectAll('.'+stackedbarClass).style('opacity', '')
            .select('.'+backgroundClass).style('fill', '');
        return this;
    };


    var _hoverItem = function(id, index) {
        svg.select(stackedbarPrefix +''+ id).selectAll('.'+backgroundClass).style('fill', 'url(#bar-shadow)')
        svg.select(stackedbarPrefix +''+ id).selectAll('.'+barClass)
            // .attr('transform', 'translate(0, 0.1)')
           // .style('filter', 'url(#drop-shadow)')
            .text(function(d){ return d.score });
        return this;
    };


    var _unhoverItem = function(id, index) {
        if(!_this.selectedItem) {
            svg.select(stackedbarPrefix +''+ id).selectAll('.'+backgroundClass).style('fill', '')
            svg.select(stackedbarPrefix +''+ id).selectAll('.'+barClass)
                // .attr('transform', 'translate(0, 0.2)')
                .style('filter', '')
                .text('');
        }
        return this;
    };


    var _clearEffects = function() {
        this.deselectAllItems();
        return this;
    };


    //  Redraw without animating when the container's size changes
    var _resize = function(containerHeight){
        if(this.isRankingDrawn) RANKING.Render.resizeCanvas(containerHeight);
        return this;
    };

    var _getHeight = function() {
        return $('.'+svgClass).height();
    };


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    Ranking.prototype = {
        build: _build,
        update: _update,
        clear: _clear,
        reset: _reset,
        selectItem: _selectItem,
        deselectAllItems : _deSelectAllItems,
        hoverItem: _hoverItem,
        unhoverItem: _unhoverItem,
        highlightItems: _highlightItems,
        clearEffects: _clearEffects,
        resize: _resize,
        getHeight: _getHeight
    };

    return Ranking;
})();


module.exports = Ranking;

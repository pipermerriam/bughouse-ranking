var app = app || {};

$(function(){
    "use-strict";

    var SinglePlayerView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.single_player,
    });

    var PlayersView = Backbone.Marionette.CollectionView.extend({
        tagName: "div",
        childView: SinglePlayerView
    });

    var GraphView = Backbone.Marionette.View.extend({
        tagName: "div",
        svg_el: null,
        getSVG: function() {
            if ( _.isNull(this.svg_el) ) {
                this.svg_el = d3.select(this.el).append('svg');
            }
            return this.svg_el;
        },
        events: {
            "click svg": "render"
        },
        render: function() {
            /*
             *  D3!
             */
            var ratings = this.model.get("ratings");
            var lineData = ratings.collect(function(rating) {
                return {
                    x: rating.getCreatedDate(),
                    y: rating.get("rating")
                };
            })
            /*
            var lineData = [{
                x: 1,
                y: 5
                    }, {
                x: 20,
                y: 20
                    }, {
                x: 40,
                y: 10
                    }, {
                x: 60,
                y: 40
                    }, {
                x: 80,
                y: 5
                    }, {
                x: 100,
                y: 60
            }];
            */
            var width = 900;
            var height = 500;
            var vis = this.getSVG()
                .attr("width", width)
                .attr("height", height)
            var margins = {
                top: 20,
                right: 20,
                left: 50,
                bottom: 20
            };
            var xMin = d3.min(lineData, function(d) {
                return d.x;
            });
            var xMax = d3.max(lineData, function(d) {
                return d.x;
            });
            var xRange = d3.scale.linear()
                .range([margins.left, width - margins.right])
                .domain([xMin, xMax]);

            var yMin = d3.min(lineData, function(d) {
                return d.y;
            });
            var yMax = d3.max(lineData, function(d) {
                return d.y;
            });
            var yRange = d3.scale.linear()
                .range([height - margins.top, margins.bottom])
                .domain([yMin, yMax]);

            var xAxis = d3.svg.axis()
                .scale(xRange)
                .tickSize(5)
                .tickSubdivide(true);
            var yAxis = d3.svg.axis()
                .scale(yRange)
                .tickSize(5)
                .orient('left')
                .tickSubdivide(true);
            vis.append('svg:g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (height - margins.bottom) + ')')
                .call(xAxis);
            vis.append('svg:g')
                .attr('class', 'y axis')
                .attr('transform', 'translate(' + (margins.left) + ',0)')
                .call(yAxis);

            var lineFunc = d3.svg.line()
                .x(function(d) {
                    return xRange(d.x);
                })
                .y(function(d) {
                    return yRange(d.y);
                })
                .interpolate('linear');
            vis.append('svg:path')
                .attr('d', lineFunc(lineData))
                .attr('stroke', 'blue')
                .attr('stroke-width', 2)
                .attr('fill', 'none');
            $('#graph').append(this.$el);
        }
    });

    app.GraphView = GraphView;
    app.PlayersView = PlayersView;
});


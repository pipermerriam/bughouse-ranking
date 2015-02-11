var app = app || {};

$(function(){
    "use-strict";

    var SinglePlayerView = Backbone.Marionette.ItemView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "change:isSelected", this.render);
        },
        tagName: "div",
        template: Handlebars.templates.single_player,
        events: {
            "click a img": "toggleSelection"
        },
        toggleSelection: function(event) {
            event.preventDefault();
            this.model.set("isSelected", !this.model.get("isSelected"));
        }
    });

    var PlayersView = Backbone.Marionette.CollectionView.extend({
        tagName: "div",
        childView: SinglePlayerView
    });

    var PlayerGraphView = Backbone.Marionette.View.extend({
        colors: {
            0: "limegreen",
            1: "blue",
            2: "blueviolet",
            3: "maroon",
            4: "red",
            5: "green",
            6: "cadetblue",
            7: "darkgoldenrod",
            8: "darkorange",
            9: "palevioletred",
            10: "dodgerblue",
            11: "fuchsia",
            12: "springgreen",
            13: "violet",
            14: "yellowgreen",
            15: "salmon",
            16: "saddlebrown",
            17: "aquamarine",
            18: "midnightblue",
            19: "lightslategray"
        },
        initialize: function(options) {
            // Listen for when a player's ratings have been fetched.
            this.listenTo(this.model, "ratings:fetched", _.bind(this.render, this));
            this.listenTo(this.model, "change:isSelected", _.bind(this.render, this));
        },
        tagName: "g",
        _ensureElement: function() {
            /*
             *  SVG elements need to be namespaced, so we must override the
             *  default DOM element creation mechanism.  Without this, the SVG
             *  silently does not render.
             */
            if (!this.el) {
                var el = document.createElementNS('http://www.w3.org/2000/svg', this.tagName);
                this.setElement(el);
            } else {
                this.setElement(this.el);
            }
        },
        render: function() {
            if ( this.model.get("isSelected") ) {
                this.renderRatings();
            } else {
                this.clearRendering();
            }
            this.trigger("render");
        },
        clearRendering: function() {
            this.$el.html('');
        },
        getRatingsData: function() {
            /*
             *  Return an array of data points for graphing.
             */
            if ( _.isUndefined(this.model.get("ratings")) ) {
                return [];
            } else {
                return this.model.get("ratings").collect(function(rating) {
                    return {
                        x: rating.getCreatedDate(),
                        y: rating.get("rating")
                    };
                });
            }
        },
        getXBounds: function(lineData) {
            if ( _.isUndefined(lineData) ) {
                lineData = this.getRatingsData();
            }
            return {
                xMin: d3.min(lineData, function(d) {return d.x;}),
                xMax: d3.max(lineData, function(d) {return d.x;})
            };
        },
        getYBounds: function(lineData) {
            if ( _.isUndefined(lineData) ) {
                lineData = this.getRatingsData();
            }
            return {
                yMin: d3.min(lineData, function(d) { return d.y; }),
                yMax: d3.max(lineData, function(d) { return d.y; })
            };
        },
        renderRatings: function() {
            /*
             *  D3!
             */
            var lineData = this.getRatingsData();
            var width = 900;
            var height = 500;
            var vis = d3.select(this.el)
                .attr("width", width)
                .attr("height", height)
            var margins = {
                top: 20,
                right: 20,
                left: 50,
                bottom: 20
            };
            var xBounds = this.getXBounds(lineData);
            var xRange = d3.time.scale.utc()
                .range([margins.left, width - margins.right])
                .domain([xBounds.xMin, xBounds.xMax]);

            var yBounds = this.getYBounds(lineData);
            var yRange = d3.scale.linear()
                .range([height - margins.top, margins.bottom])
                .domain([yBounds.yMin, yBounds.yMax]);

            var lineFunc = d3.svg.line()
                .interpolate("cardinal")
                .x(function(d) {
                    return xRange(d.x);
                })
                .y(function(d) {
                    return yRange(d.y);
                });
            var lineColor = this.colors[this.model.id % 20];
            vis.append('svg:path')
                .attr('d', lineFunc(lineData))
                .attr('stroke', lineColor)
                .attr('stroke-width', 2)
                .attr('fill', 'none');
            var points = vis.selectAll('.point').data(lineData)
                .enter()
                .append("svg:circle")
                .attr("stroke", "black")
                .attr("fill", function(d, i) { return "black" })
                .attr("cx", function(d, i) { return xRange(d.x) })
                .attr("cy", function(d, i) { return yRange(d.y) })
                .attr("r", function(d, i) { return 2 });
        }
    });

    var GraphView = Backbone.Marionette.CollectionView.extend({
        initialize: function(options) {
            this.axis_el = d3.select(this.el).append('g');
            this.on("childview:render", this.renderAxis);
        },
        tagName: "svg",
        childView: PlayerGraphView,
        _ensureElement: function() {
            /*
             *  SVG elements need to be namespaced, so we must override the
             *  default DOM element creation mechanism.  Without this, the SVG
             *  silently does not render.
             */
            if (!this.el) {
                var el = document.createElementNS('http://www.w3.org/2000/svg', this.tagName);
                $(el).attr({
                    class: "main",
                    width: 900,
                    height: 500
                });
                this.setElement(el);
            } else {
                this.setElement(this.el);
            }
        },
        template: Handlebars.templates.graph,
        getDefaultMinDate: function() {
            var MONTH_1 = 31 * 24 * 60 * 60 * 1000;
            return new Date(new Date() - MONTH_1);
        },
        getSelectedChildren: function() {
            return this.children.filter(function(child) {
                return child.model.get("isSelected");
            });
        },
        getXBounds: function() {
            var childBounds = this.getSelectedChildren().map(function(child) {
                return child.getXBounds();
            });
            var defaultMinDate = this.getDefaultMinDate();
            return {
                xMin: d3.min(childBounds, function(b) {return b.xMin;}) || defaultMinDate,
                xMax: d3.max(childBounds, function(b) {return b.xMax;}) || new Date(),
            }
        },
        getYBounds: function() {
            var childBounds = this.getSelectedChildren().map(function(child) {
                return child.getYBounds();
            });
            return {
                yMin: d3.min(childBounds, function(b) {return b.yMin;}) || 900,
                yMax: d3.max(childBounds, function(b) {return b.yMax;}) || 1100,
            }
        },
        renderAxis: function() {
            // Clear the axis.
            $(this.axis_el).html('');
            this.axis_el.html('');
            var vis = this.axis_el;

            var width = 900;
            var height = 500;
            var margins = {
                top: 20,
                right: 20,
                left: 50,
                bottom: 20
            };


            var xBounds = this.getXBounds();
            var xRange = d3.time.scale.utc()
                .range([margins.left, width - margins.right])
                .domain([xBounds.xMin, xBounds.xMax]);

            var yBounds = this.getYBounds();
            var yRange = d3.scale.linear()
                .range([height - margins.top, margins.bottom])
                .domain([yBounds.yMin, yBounds.yMax]);

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
        },
        onRender: function() {
            this.renderAxis();
        }
    });

    app.PlayerGraphView = PlayerGraphView;
    app.GraphView = GraphView;
    app.PlayersView = PlayersView;
});


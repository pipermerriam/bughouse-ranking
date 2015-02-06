var app = app || {};

$(function(){
    "use-strict";

    var GraphLayout = Backbone.Marionette.LayoutView.extend({
        initialize: function(options) {
            this.application = options.application;
        },
        el: "#application",
        regions: {
            players: "#players",
            arst: "#arst",
            graph: "#graph"
        },
    });

    app.GraphLayout = GraphLayout;
});

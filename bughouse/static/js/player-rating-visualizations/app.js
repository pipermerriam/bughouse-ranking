var app = app || {};

$(function(){
    "use-strict";

    var PlayerRatingsVisualizationApp = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.players = new app.Players(options.players || []);
        },
        setupLayout: function(game) {
            this.graph_layout = new app.GraphLayout({
                application: this
            });
            this.graph_layout.players.show(new app.PlayersView({
                collection: this.players
            }));

            var graphView = new app.GraphView({
                collection: this.players
            });
            this.graph_layout.graph.show(graphView);

            var controlsView = new app.ControlsView({
                model: new Backbone.Model({dataKey: "overall:overall"})
            });
            this.graph_layout.controls.show(controlsView);

            graphView.listenTo(controlsView.model, "change:dataKey", _.bind(graphView.keyChanged, graphView));
        },
        start: function(options) {
            this.setupLayout();
        }
    });

    app.PlayerRatingsVisualizationApp = PlayerRatingsVisualizationApp;
});

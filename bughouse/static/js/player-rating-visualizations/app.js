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
            this.graph_layout.graph.show(new app.GraphView({
                collection: this.players
            }));
        },
        start: function(options) {
            this.setupLayout();
        }
    });

    app.PlayerRatingsVisualizationApp = PlayerRatingsVisualizationApp;
});
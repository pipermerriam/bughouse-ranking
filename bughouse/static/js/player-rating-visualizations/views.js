var app = app || {};

$(function(){
    "use-strict";

    var SinglePlayerView = Backbone.Marionette.ItemView({
        tagName: "div",
        template: Handlebars.templates.single_player
    });

    var PlayersView = Backbone.Marionette.CollectionView({
        childView: SinglePlayerView,
        tagName: "div",
    });

    var GraphView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
    });

    app.GraphView = GraphView;
});


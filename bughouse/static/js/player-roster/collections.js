var app = app || {};

$(function(){
    "use-strict";

    var Players = Backbone.Collection.extend({
        model: app.Player,
    });

    app.Players = Players;
});

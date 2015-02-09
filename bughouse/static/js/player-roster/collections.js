var app = app || {};

$(function(){
    "use-strict";

    var Players = Backbone.Collection.extend({
        model: app.Player,
        comparator: "name"
    });

    var Messages = Backbone.Collection.extend({
        model: app.Message,
        comparator: "createdDate"
    });

    app.Players = Players;
    app.Messages = Messages;
});

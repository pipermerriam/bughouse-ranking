var app = app || {};

$(function(){
    "use-strict";

    var SinglePlayerView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.roster_player
    });

    var RosterView = Backbone.Marionette.CollectionView.extend({
        tagName: "div",
        template: Handlebars.templates.roster,
        childView: SinglePlayerView
    });

    var PlayerFormView = Backbone.Marionette.ItemView.extend({
        tagName: "form",
        template: Handlebars.templates.player_form
    });

    app.RosterView = RosterView;
    app.PlayerFormView = PlayerFormView;
});



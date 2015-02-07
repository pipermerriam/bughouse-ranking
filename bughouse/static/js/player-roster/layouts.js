var app = app || {};

$(function(){
    "use-strict";

    var RosterLayout = Backbone.Marionette.LayoutView.extend({
        tagName: "div",
        el: "#application",
        regions: {
            roster: "#roster",
            player_form: "#player-form"
        },
    });

    app.RosterLayout = RosterLayout;
});


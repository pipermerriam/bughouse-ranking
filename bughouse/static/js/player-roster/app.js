var app = app || {};

$(function(){
    "use-strict";

    var PlayerRosterApp = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.players = new app.Players(options.players || []);
        },
        setupLayout: function(game) {
            this.roster_layout = new app.RosterLayout();
            this.roster_layout.roster.show(new app.RosterView({
                collection: this.players
            }));
            this.roster_layout.player_form.show(new app.PlayerFormView(new app.Player()));
        },
        start: function(options) {
            this.setupLayout();
        }
    });

    app.PlayerRosterApp = PlayerRosterApp;
});

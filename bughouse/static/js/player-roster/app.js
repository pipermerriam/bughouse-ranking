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
            this.roster_layout.player_form.show(new app.PlayerFormView({
                model: new app.Player()
            }));
            var form_view = this.roster_layout.player_form.currentView;
            var roster_view = this.roster_layout.roster.currentView;
            roster_view.listenTo(form_view, "model:created", _.bind(roster_view.addNewPlayer, roster_view));
        },
        start: function(options) {
            this.setupLayout();
        }
    });

    app.PlayerRosterApp = PlayerRosterApp;
});

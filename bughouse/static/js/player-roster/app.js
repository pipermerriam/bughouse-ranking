var app = app || {};

$(function(){
    "use-strict";

    var PlayerRosterApp = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.players = new app.Players(options.players || []);
        },
        setupLayout: function(game) {
            // Layout
            this.roster_layout = new app.RosterLayout();
            // Views
            var rosterView = new app.RosterView({
                collection: this.players
            });
            var formView = this.setupPlayerForm();

            // Put views in layouts
            this.roster_layout.roster.show(rosterView);
            this.roster_layout.player_form.show(formView);

            // Listen to the form submitting.
            this.listenTo(formView, "model:created", _.bind(this.addNewPlayer, this));
        },
        setupPlayerForm: function(player) {
            if ( _.isUndefined(player) ) {
                player = new app.Player();
            }
            var formView = new app.PlayerFormView({
                model: player
            });
            return formView;
        },
        start: function(options) {
            this.setupLayout();
        },
        addNewPlayer: function(player) {
            this.players.add(player);
            this.roster_layout.player_form.show(this.setupPlayerForm());
        }
    });

    app.PlayerRosterApp = PlayerRosterApp;
});

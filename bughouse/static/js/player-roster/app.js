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
            this.messagesView = new app.MessagesView({
                collection: new app.Messages()
            })
            var rosterView = new app.RosterView({
                collection: this.players
            });
            var formView = this.setupPlayerForm();

            // Put views in layouts
            this.roster_layout.roster.show(rosterView);
            this.roster_layout.player_form.show(formView);
            this.roster_layout.messages.show(this.messagesView);

            // Listen to the form submitting.
            this.listenTo(formView, "model:created", _.bind(this.addNewPlayer, this));
            this.listenTo(formView, "messages:add", _.bind(this.addMessage, this));
            this.listenTo(rosterView, "player:edit", _.bind(this.editPlayer, this));
        },
        editPlayer: function(player) {
            var editFormView = this.setupPlayerForm(player);
            this.roster_layout.player_form.show(editFormView);
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
        addMessage: function(options) {
            this.messagesView.collection.add(new app.Message(options));
        },
        addNewPlayer: function(player) {
            this.players.add(player);
            this.roster_layout.player_form.show(this.setupPlayerForm());
        }
    });

    app.PlayerRosterApp = PlayerRosterApp;
});

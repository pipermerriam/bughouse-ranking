var app = app || {};

$(function(){
    "use-strict";

    var ReportGameApp = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.players = new Backbone.Collection(options.players || []);
            this.recent_games = new app.Games(options.recent_games || []);
        },
        setupLayout: function(game) {
            this.game_form_layout = new app.GameReportFormLayout({
                application: this
            });
            this.game_form_layout.model = game;
            this.game_form_layout.listenTo(game, "game:submit", _.bind(this.game_form_layout.submit, this.game_form_layout));
            this.listenTo(game, "sync", this.addGameToCollection);
            $("#report-game-form").append(this.game_form_layout.$el);
            this.game_form_layout.render();
            this.listenTo(this.game_form_layout, "form:success", this.resetForm);
        },
        initializeRecentGames: function() {
            this.games_view = new app.RecentGamesView({
                collection: this.recent_games
            });
            this.games_view.render();
            this.listenTo(this.games_view, "model:edit", this.editGame);
        },
        setupPlayerSelects: function(game) {
            /*
             * Setup the four select a player views.
             */
            this.game_form_layout.winning_team.show(new app.PlayerSelectView({
                isWinners: true,
                model: game,
                collection: this.players
            }));
            this.game_form_layout.losing_team.show(new app.PlayerSelectView({
                isWinners: false,
                model: game,
                collection: this.players
            }));
        },
        setupLossTypeSelect: function(game) {
            this.game_form_layout.loss_type.show(new app.LossTypeView({
                model: game
            }));
        },
        setupLosingColorSelect: function(game) {
            this.game_form_layout.losing_color.show(new app.LosingColorView({
                model: game
            }));
        },
        initializeForm: function(game) {
            this.setupLayout(game);
            this.setupPlayerSelects(game);
            this.setupLossTypeSelect(game);
            this.setupLosingColorSelect(game);
        },
        addGameToCollection: function(game) {
            this.recent_games.add(game);
        },
        editGame: function(game) {
            this.game_form_layout.destroy();
            this.initializeForm(game);
        },
        resetForm: function(game) {
            this.game_form_layout.destroy();
            this.initializeForm(new app.Game());
        },
        start: function(options) {
            this.initializeForm(new app.Game());
            this.initializeRecentGames();
        }
    });

    app.ReportGameApp = ReportGameApp;
});

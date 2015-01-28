var app = app || {};

$(function(){
    "use-strict";

    var ReportGameApp = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.setupLayout(options);
            this.listenTo(this.game_report_layout, "form:success", this.resetForm);
            this.listenTo(this.game_report_layout, "form:success", this.addGameToCollection);
        },
        setupLayout: function(options) {
            this.game_report_layout = new app.GameReportFormLayout({
                application: this
            });
            $("#report-game-form").append(this.game_report_layout.$el);
            this.game_report_layout.render();
        },
        initializeRecentGamesView: function(options) {
            this.games_view = new app.RecentGamesView({
                collection: this.recent_games
            });
            this.games_view.render();
        },
        initializeFormViews: function(options) {
            var report = this.game_report_layout.model = new app.Game({
                players: this.players
            });
            this.game_report_layout.winning_team_white.show(new app.PlayerSelectView({
                playerColor: "White",
                teamLabel: "Winning",
                modelAttribute: "winning_team_white",
                model: report
            }));
            this.game_report_layout.winning_team_black.show(new app.PlayerSelectView({
                playerColor: "Black",
                teamLabel: "Winning",
                modelAttribute: "winning_team_black",
                model: report
            }));
            this.game_report_layout.losing_team_white.show(new app.PlayerSelectView({
                playerColor: "White",
                teamLabel: "Losing",
                modelAttribute: "losing_team_white",
                model: report
            }));
            this.game_report_layout.losing_team_black.show(new app.PlayerSelectView({
                playerColor: "Black",
                teamLabel: "Losing",
                modelAttribute: "losing_team_black",
                model: report
            }));
            this.game_report_layout.loss_type.show(new app.LossTypeView({
                model: report
            }));
            this.game_report_layout.losing_color.show(new app.LosingColorView({
                model: report
            }));
        },
        addGameToCollection: function(game) {
            this.recent_games.add(game);
        },
        resetForm: function(game) {
            var options = {
                players: this.players
            };
            this.game_report_layout.destroy();
            this.setupLayout(options);
            this.initializeFormViews(options);
        },
        start: function(options) {
            this.players = new Backbone.Collection(options.players);
            this.recent_games = new app.Games(options.recent_games);
            this.initializeFormViews(options);
            this.initializeRecentGamesView(options);
        }
    });

    app.ReportGameApp = ReportGameApp;
});

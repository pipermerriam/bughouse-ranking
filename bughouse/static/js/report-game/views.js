var app = app || {};

$(function(){
    "use-strict";

    var PlayerSelectView = Backbone.Marionette.ItemView.extend({
        initialize: function(options) {
            this.errors = [];
            this.listenTo(this.model, "change", this.render);
            this.listenTo(this.model, "validate", this.validate);
        },
        tagName: "div",
        template: Handlebars.templates.player_select,
        /*
         *  Validation
         */
        hasErrors: function() {
            return Boolean(this.errors.length);
        },
        validate: function() {
            this.errors = [];
            if ( !this.hasSelection() ) {
                this.errors.push("Please select a player");
            }
            this.render();
        },
        /*
         *  Template Helpers
         */
        playerChanged: function(e) {
            var playerId = e.currentTarget.value;
            this.model.set(this.options.modelAttribute, playerId);
        },
        hasSelection: function() {
            return _.isObject(this.selectedPlayer());
        },
        selectedPlayer: function() {
            var playerId = this.model.get(this.options.modelAttribute);
            return this.model.getPlayer(playerId);
        },
        playerChoices: function() {
            var availablePlayers = this.model.unselectedPlayers();
            if ( this.hasSelection() ) {
                availablePlayers.push(this.selectedPlayer());
            }
            return availablePlayers;
        },
        templateHelpers: function() {
            return {
                errors: this.errors,
                hasErrors: this.hasErrors(),
                teamLabel: this.options.teamLabel,
                selectedPlayer: this.selectedPlayer() ? this.serializeModel(this.selectedPlayer()) : null,
                hasSelection: this.hasSelection(),
                playerColor: this.options.playerColor,
                playerChoices: _.map(this.playerChoices(), this.serializeModel)
            };
        },
        events: {
            "change select": "playerChanged"
        }
    });

    Handlebars.registerHelper("isPlayerSelected", function(selectedPlayer) {
        /*
         *  Helper for determining which (if any) option should be selected.
         */
        if ( !_.isObject(selectedPlayer) ) {
            return "";
        }
        else if ( selectedPlayer.id === this.id ) {
            return " selected=\"selected\"";
        } else {
            return "";
        }
    });

    LosingColorView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.losing_color,
        radioChanged: function(e) {
            this.model.set("losing_color", e.currentTarget.value);
        },
        events: {
            "change input[type=\"radio\"]": "radioChanged"
        }
    });

    LossTypeView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.loss_type,
        radioChanged: function(e) {
            this.model.set("loss_type", e.currentTarget.value);
        },
        events: {
            "change input[type=\"radio\"]": "radioChanged"
        }
    });

    RecentGameView = Backbone.Marionette.ItemView.extend({
        tagName: "tr",
        template: Handlebars.templates.game_row,
        destroyGame: function() {
            this.model.destroy();
        },
        editGame: function() {
            this.trigger("model:edit", this.model);
        },
        events: {
            "click button.delete": "destroyGame",
            "click button.edit": "editGame"
        }
    });

    RecentGamesView = Backbone.Marionette.CompositeView.extend({
        initialize: function() {
            this.on("childview:model:edit", this.editGame);
        },
        el: "#recent-games",
        template: Handlebars.templates.recent_games,
        childView: RecentGameView,
        childViewContainer: "tbody",
        editGame: function(childView, game) {
            this.trigger("model:edit", game);
        }
    });

    app.RecentGamesView = RecentGamesView;
    app.PlayerSelectView = PlayerSelectView;
    app.LosingColorView = LosingColorView;
    app.LossTypeView = LossTypeView;
});

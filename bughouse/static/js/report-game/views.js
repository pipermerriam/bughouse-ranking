var app = app || {};

$(function(){
    "use-strict";

    var PlayerIconView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.player_icon,
        toggleSelection: function(e) {
            var playerId = this.model.id;
            this.trigger("toggleSelection", playerId);
        },
        templateHelpers: function() {
            return {
                isPlayerSelected: this.options.isPlayerSelected(this.model.id),
                isPlayerAvailable: this.options.isPlayerAvailable(this.model.id)
            };
        },
        events: {
            "click div.player-container.available": "toggleSelection",
            "click div.player-container.selected": "toggleSelection"
        }
    });

    var PlayerSelectView = Backbone.Marionette.CompositeView.extend({
        initialize: function(options) {
            this.errors = [];
            this.listenTo(this.model, "change", this.render);
            this.listenTo(this.model, "validate", this.validate);
            this.on("childview:toggleSelection", this.toggleSelection);
        },
        tagName: "div",
        template: Handlebars.templates.player_select,
        childView: PlayerIconView,
        childViewContainer: 'div.players',
        /*
         *
         */
        toggleSelection: function(childView, playerId) {
            if ( playerId === this.model.get(this.getWhiteAttr()) ) {
                this.model.set(this.getWhiteAttr(), null);
            } else if ( playerId === this.model.get(this.getBlackAttr()) ) {
                this.model.set(this.getBlackAttr(), null);
            } else {
                this.setFirstEmptyColor(playerId);
            }
            console.log(this.model.attributes)
        },
        setFirstEmptyColor: function(playerId) {
            if ( !this.hasWhiteSelection() ) {
                this.model.set(this.getWhiteAttr(), playerId);
            } else if ( !this.hasBlackSelection() ) {
                this.model.set(this.getBlackAttr(), playerId);
            }
        },
        /*
         *  Validation
         */
        hasErrors: function() {
            return Boolean(this.errors.length);
        },
        validate: function() {
            this.errors = [];
            if ( !this.hasWhiteSelection() || !this.hasBlackSelection() ) {
                this.errors.push("Please select a player");
            }
            this.render();
        },
        /*
         *  Child View Stuff
         */
        isPlayerSelected: function(playerId) {
            if ( this.hasWhiteSelection() ) {
                if ( this.selectedWhitePlayer().id === playerId ) {
                    return true;
                }
            }
            if ( this.hasBlackSelection() ) {
                if ( this.selectedBlackPlayer().id === playerId ) {
                    return true;
                }
            }
            return false;
        },
        isPlayerAvailable: function(playerId) {
            return _.contains(_.pluck(this.model.unselectedPlayers(), 'id'), playerId);
        },
        childViewOptions: function() {
            return {
                isPlayerSelected: _.bind(this.isPlayerSelected, this),
                isPlayerAvailable: _.bind(this.isPlayerAvailable, this)
            };
        },
        /*
         *  Template Helpers
         */
        getPrefix: function() {
            return this.options.isWinners ? "winning_team_" : "losing_team_";
        },
        getWhiteAttr: function() {
            return this.getPrefix() + "white";
        },
        getBlackAttr: function() {
            return this.getPrefix() + "black";
        },
        teamDisplayName: function() {
            return this.options.isWinners ? "Winning" : "Losing";
        },
        selectedWhitePlayer: function() {
            var playerId = this.model.get(this.getWhiteAttr());
            return this.model.getPlayer(playerId);
        },
        selectedBlackPlayer: function() {
            var playerId = this.model.get(this.getBlackAttr());
            return this.model.getPlayer(playerId);
        },
        hasWhiteSelection: function() {
            return _.isObject(this.selectedWhitePlayer());
        },
        hasBlackSelection: function() {
            return _.isObject(this.selectedBlackPlayer());
        },
        hasBothSelections: function() {
            return this.hasWhiteSelection() && this.hasBlackSelection();
        },
        templateHelpers: function() {
            return {
                errors: this.errors,
                hasErrors: this.hasErrors(),
                teamDisplayName: this.teamDisplayName(),
                hasWhiteSelection: this.hasWhiteSelection(),
                hasBlackSelection: this.hasBlackSelection(),
                hasBothSelections: this.hasBothSelections(),
                selectedWhitePlayer: this.selectedWhitePlayer(),
                selectedBlackPlayer: this.selectedBlackPlayer(),
            };
        },
    });

    LosingColorView = Backbone.Marionette.ItemView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "change", this.render);
        },
        tagName: "div",
        template: Handlebars.templates.losing_color,
        radioChanged: function(e) {
            this.model.set("losing_color", e.currentTarget.value);
        },
        swapSelection: function() {
            var whiteSelection = this.model.get("losing_team_white");
            var blackSelection = this.model.get("losing_team_black");
            this.model.set({
                losing_team_white: blackSelection,
                losing_team_black: whiteSelection
            });
        },
        setWhiteAsLoser: function() {
            this.model.set("losing_color", "white");
        },
        setBlackAsLoser: function() {
            this.model.set("losing_color", "black");
        },
        events: {
            "click a.swap": "swapSelection",
            "click a.white": "setWhiteAsLoser",
            "click a.black": "setBlackAsLoser"
        }
    });

    LossTypeView = Backbone.Marionette.ItemView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "change:loss_type", this.render);
        },
        tagName: "div",
        template: Handlebars.templates.loss_type,
        setCheckmate: function() {
            this.model.set("loss_type", "checkmate");
        },
        setTime: function() {
            this.model.set("loss_type", "time");
        },
        setSwindle: function() {
            this.model.set("loss_type", "swindle");
        },
        setImminentDeath: function() {
            this.model.set("loss_type", "imminent-death");
        },
        templateHelpers: function() {
            return {
                'isCheckmate': this.model.get("loss_type") === "checkmate",
                'isTime': this.model.get("loss_type") === "time",
                'isSwindle': this.model.get("loss_type") === "swindle",
                'isImminentDeath': this.model.get("loss_type") === "imminent-death"
            };
        },
        events: {
            "click button.checkmate": "setCheckmate",
            "click button.time": "setTime",
            "click button.swindle": "setSwindle",
            "click button.imminent-death": "setImminentDeath",
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
        setFocus: function() {
            this.el.focus();
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
        onRenderCollection: function() {
            this.on("add", this.setFocus);
        },
        setFocus: function(model, collection) {
            model.listenToOnce("render", model.setFocus);
        },
        editGame: function(childView, game) {
            this.trigger("model:edit", game);
        }
    });

    app.RecentGamesView = RecentGamesView;
    app.PlayerSelectView = PlayerSelectView;
    app.LosingColorView = LosingColorView;
    app.LossTypeView = LossTypeView;
});

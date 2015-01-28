var app = app || {};

$(function(){
    "use-strict";

    var Game = Backbone.Model.extend({
        defaults: {
            created_at: null,
            updated_at: null,
            winning_team_white: null,
            winning_team_black: null,
            losing_team_white: null,
            losing_team_black: null,
            losing_color: null,
            loss_type: null
        },
        urlRoot: "/api/v1/games/",
        url: function() {
            if ( this.isNew() ) {
                return this.urlRoot;
            } else {
                return this.urlRoot + this.id + "/";
            }
        },
        comparator: function(a, b) {
            var date_a = a.getCreatedDate();
            var date_b = b.getCreatedDate();

            if ( date_a === date_b ) {
                return 0;
            } else if ( date_a > date_b ){
                return -1;
            } else {
                return 1;
            }
        },
        getCreatedDate: function() {
            var createdDate = this.get("created_at");
            return _.isNull(createdDate) ? null : new Date(createdDate);
        },
        isValid: function() {
            this.trigger("validate");
            if ( !(this.selectedPlayers().length === 4) ) {
                return false;
            }
            if ( !_.isString(this.get("losing_color")) ) {
                return false;
            }
            return true;
        },
        toJSON: function() {
            return {
                id: this.id,
                winning_team_white: this.get("winning_team_white"),
                winning_team_black: this.get("winning_team_black"),
                losing_team_white: this.get("losing_team_white"),
                losing_team_black: this.get("losing_team_black"),
                losing_color: this.get("losing_color"),
                loss_type: this.get("loss_type")
            };
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "lossTypeOptions",
            "losingColorOptions",
            "isEditable",
        ],
        isEditable: function() {
            if ( _.isNull(this.get("created_at")) ) {
                return true;
            } else {
                var createdDate = new Date(this.get("created_at"));
                var MINUTES_5 = 60 * 5 * 1000;
                return new Date() - createdDate < MINUTES_5;
            }
        },
        getPlayer: function(playerId) {
            return this.get("players").get(playerId);
        },
        selectedPlayers: function() {
            var selected_player_ids = _.reject(
                [
                    this.get("winning_team_white"),
                    this.get("winning_team_black"),
                    this.get("losing_team_white"),
                    this.get("losing_team_black")
                ],
                _.isNull
            );
            return _.map(selected_player_ids, _.bind(this.getPlayer, this));
        },
        unselectedPlayers: function() {
            var players = this.get("players");
            return players.difference(this.selectedPlayers());
        },
        lossTypeOptions: function() {
            var selectedValue = this.get("loss_type");
            return [
                {name: "Checkmate", value: "checkmate", isSelected: (selectedValue === "checkmate")},
                {name: "Time", value: "time", isSelected: (selectedValue === "time")},
                {name: "Swindle", value: "swindle", isSelected: (selectedValue === "swindle")},
                {name: "Imminent Death", value: "imminent-death", isSelected: (selectedValue === "imminent-death")}
            ];
        },
        losingColorOptions: function() {
            var selectedColor = this.get("losing_color");
            return [
                {name: "White", value: "white", isSelected: (selectedColor === "white")},
                {name: "Black", value: "black", isSelected: (selectedColor === "black")},
            ]
        }
    });

    app.Game = Game;
});

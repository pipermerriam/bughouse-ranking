var app = app || {};

$(function(){
    "use-strict";

    var Players = Backbone.Collection.extend({
        model: app.Player,
    });

    var PlayerRatings = Backbone.Collection.extend({
        initialize: function(collection, options) {
            this.player = options.player;
        },
        model: app.PlayerRating,
        urlRoot: function() {
            var player = this.player;
            var playerUrlRoot = player.url();
            return playerUrlRoot + 'ratings/';
        },
        url: function() {
            return this.urlRoot();
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
        }
    });

    app.Players = Players;
    app.PlayerRatings = PlayerRatings;
});


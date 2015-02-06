var app = app || {};

$(function(){
    "use-strict";

    var Player = Backbone.Model.extend({
        initialize: function(options) {
            if ( _.isUndefined(options.ratings) ) {
                var ratings = new app.PlayerRatings([], {player: this});
                ratings.fetch();
            } else {
                var ratings = options.ratings;
            }
            this.set("ratings", ratings);
        },
        urlRoot: "/api/v1/players/",
        url: function() {
            if ( this.isNew() ) {
                return this.urlRoot;
            } else {
                return this.urlRoot + this.id + "/";
            }
        }
    });

    var PlayerRating = Backbone.Model.extend({
        getCreatedDate: function() {
            var createdDate = this.get("created_at");
            return _.isNull(createdDate) ? null : new Date(createdDate);
        }
    });

    app.Player = Player;
    app.PlayerRating = PlayerRating;
});


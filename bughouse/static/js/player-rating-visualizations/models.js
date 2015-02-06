var app = app || {};

$(function(){
    "use-strict";

    var Player = Backbone.Model.extend({
        defaults: {
            isSelected: false
        },
        initialize: function(options) {
            if ( _.isUndefined(options.ratings) ) {
                var ratings = new app.PlayerRatings([], {player: this});
                ratings.fetch({
                    success: _.bind(this.ratingsFetchSucces, this)
                });
            } else {
                var ratings = options.ratings;
            }
            this.set("ratings", ratings);
        },
        ratingsFetchSucces: function(collection, response, options) {
            /*
             *  Used as a success callback for `fetch` to signal that ratings
             *  have been loaded.
             */
            this.trigger("ratings:fetched");
        },
        getRatingsData: function() {
            /*
             *  Return an array of data points for graphing.
             */
            if ( _.isUndefined(this.get("ratings")) ) {
                return [];
            } else {
                return this.get("ratings").collect(function(rating) {
                    return {
                        x: rating.getCreatedDate(),
                        y: rating.get("rating")
                    };
                });
            }
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


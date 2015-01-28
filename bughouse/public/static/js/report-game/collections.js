var app = app || {};

$(function(){
    "use-strict";

    var Games = Backbone.Collection.extend({
        model: app.Game,
        urlRoot: "/api/v1/games/",
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

    app.Games = Games;
});

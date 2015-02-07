var app = app || {};

$(function(){
    "use-strict";

    var Player = Backbone.Model.extend({
        urlRoot: "/api/v1/players/",
        url: function() {
            if ( this.isNew() ) {
                return this.urlRoot;
            } else {
                return this.urlRoot + this.id + "/";
            }
        }
    });

    app.Player = Player;
});

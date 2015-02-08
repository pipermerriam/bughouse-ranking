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

    var Message = Backbone.Model.extend({
        defaults: function() {
            return {
                message: null,
                level: "primary",
                createdDate: new Date(),
                isDismissable: true
            }
        },
        levels: {
            primary: "primary",
            success: "success",
            info: "info",
            warning: "warning",
            danger: "danger",
        },
        exportable: [
            "cssClasses"
        ],
        cssClasses: function() {
            var classes = [];
            classes.push("bg-" + this.get("level"));
            return classes.join(" ");
        }
    });

    app.Player = Player;
    app.Message = Message;
});

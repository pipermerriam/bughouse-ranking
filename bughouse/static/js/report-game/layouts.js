var app = app || {};

$(function(){
    "use-strict";

    var GameReportFormLayout = Backbone.Marionette.LayoutView.extend({
        initialize: function(options) {
            this.application = options.application
        },
        tagName: "div",
        template: Handlebars.templates.game_form,
        regions: {
            winning_team: '#winning-team-selection',
            losing_team: '#losing-team-selection',
            losing_color: '#losing-team-color',
            loss_type: "#loss-type"
        },
        submit: function(e) {
            if ( this.model.isValid() ) {
                this.model.save();
                this.trigger("form:success", this.model)
            } else {
                return;
            }
        },
        events: {
            "click button[type=\"button\"]": "submit"
        }
    });

    app.GameReportFormLayout = GameReportFormLayout;
});

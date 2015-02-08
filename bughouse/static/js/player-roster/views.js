var app = app || {};

$(function(){
    "use-strict";

    var SinglePlayerView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.roster_player
    });

    var RosterView = Backbone.Marionette.CollectionView.extend({
        tagName: "div",
        template: Handlebars.templates.roster,
        childView: SinglePlayerView
    });

    var MessageView = Backbone.Marionette.ItemView.extend({
        tagName: "div",
        template: Handlebars.templates.message
    })

    var MessagesView = Backbone.Marionette.CollectionView.extend({
        tagName: "div",
        template: Handlebars.templates.messages,
        childView: MessageView
    });

    var PlayerFormView = Backbone.Marionette.ItemView.extend({
        defaults: {
            name: null,
            icon: null,
            icon_filename: null,
            icon_url: null
        },
        tagName: "form",
        template: Handlebars.templates.player_form,
        events: {
            "change input": "formChanged",
            "click button": "submit"
        },
        ui: {
            submit_button: 'button.submit',
        },
        formChanged: function(event) {
            var el = $(event.currentTarget);
            if ( el.attr("name") === "name" ){
                this.model.set("name", el.val());
            } else if ( el.attr("name") === "icon" ) {
                this.handleIconSelect(event);
            }
        },
        /*
         *  File upload stuff
         */
        onIconLoad: function(readerEvt) {
            this.model.set("icon", btoa(readerEvt.target.result));
        },
        onIconLoadStart: function(readerEvt) {
            this.ui.submit_button.prop("disabled", true);
        },
        onIconLoadEnd: function(readerEvt) {
            this.ui.submit_button.prop("disabled", false);
        },
        handleIconSelect: function(event) {
            var files = event.target.files;
            var file = files[0];

            if (files && file) {
                this.model.set("icon_filename", file.name)
                var reader = new FileReader();

                reader.onload = _.bind(this.onIconLoad, this);
                reader.onloadstart = _.bind(this.onIconLoadStart, this);
                reader.onloadend = _.bind(this.onIconLoadEnd, this);

                reader.readAsBinaryString(file);
            } else {
                this.set("icon", null);
            }
        },
        submit: function(event) {
            event.preventDefault();
            var data = this.model.toJSON();
            var options = {};
            if ( this.model.isNew() ) {
                options.success = _.bind(function(){
                    this.trigger("model:created", this.model, this);
                }, this);
            }
            this.model.save(data, options);
        }
    });

    app.RosterView = RosterView;
    app.PlayerFormView = PlayerFormView;
});



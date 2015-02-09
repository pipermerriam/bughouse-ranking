var app = app || {};

$(function(){
    "use-strict";

    /*
     * https://github.com/hashchange/backbone.marionette.export#enabling-strict-mode
     *
     * Enable "strict" mode for `backbone.marionette.export` so that an error
     * is thrown when either:
     *
     * - something declared exportable does not exist.
     * - a model property is declared exportable.
     */
    Backbone.Model.prototype.export.global.strict = true;
});


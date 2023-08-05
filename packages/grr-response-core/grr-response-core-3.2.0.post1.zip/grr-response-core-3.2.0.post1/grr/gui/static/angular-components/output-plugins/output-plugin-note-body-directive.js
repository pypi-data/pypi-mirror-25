'use strict';

goog.provide('grrUi.outputPlugins.outputPluginNoteBodyDirective.OutputPluginNoteBodyController');
goog.provide('grrUi.outputPlugins.outputPluginNoteBodyDirective.OutputPluginNoteBodyDirective');


goog.scope(function() {

/**
 * Controller for OutputPluginNoteBodyDirective.
 *
 * @constructor
 * @param {!angular.Scope} $scope
 * @param {!angular.$compile} $compile
 * @param {!angular.jQuery} $element
 * @param {!grrUi.core.semanticRegistry.SemanticRegistryService}
 *     grrOutputPluginsDirectivesRegistryService
 * @ngInject
 */
grrUi.outputPlugins.outputPluginNoteBodyDirective
    .OutputPluginNoteBodyController = function(
        $scope, $compile, $element,
        grrOutputPluginsDirectivesRegistryService) {
  /** @private {!angular.Scope} */
  this.scope_ = $scope;

  /** @type {Object} */
  this.scope_.outputPlugin;

  /** @private {!angular.$compile} */
  this.compile_ = $compile;

  /** @private {!angular.jQuery} */
  this.element_ = $element;

  /** @private {!grrUi.core.semanticRegistry.SemanticRegistryService} */
  this.grrOutputPluginsDirectivesRegistryService_ =
      grrOutputPluginsDirectivesRegistryService;

  this.scope_.$watch('outputPlugin',
                     this.onOutputPluginChange_.bind(this));
};
var OutputPluginNoteBodyController =
    grrUi.outputPlugins.outputPluginNoteBodyDirective
    .OutputPluginNoteBodyController;



/**
 * Converts camelCaseStrings to dash-delimited-strings.
 *
 * @param {string} directiveName String to be converted.
 * @return {string} Converted string.
 */
OutputPluginNoteBodyController.prototype.camelCaseToDashDelimited = function(
    directiveName) {
  return directiveName.replace(/([a-z\d])([A-Z])/g, '$1-$2').toLowerCase();
};


/**
 * Handles changes in descriptor or state.
 *
 * @private
 */
OutputPluginNoteBodyController.prototype.onOutputPluginChange_ = function() {
  if (angular.isDefined(this.scope_['outputPlugin'])) {
    var descriptor =
        this.scope_['outputPlugin']['value']['plugin_descriptor'];
    var pluginName = descriptor['value']['plugin_name']['value'];

    var directive = this.grrOutputPluginsDirectivesRegistryService_
        .findDirectiveForMro([pluginName]);

    if (angular.isDefined(directive)) {
      var element = angular.element('<span />');
      element.html('<' +
        this.camelCaseToDashDelimited(directive.directive_name) +
        ' output-plugin="outputPlugin" />');

      var template = this.compile_(element);
      template(this.scope_, function(cloned, opt_scope) {
        this.element_.html('');
        this.element_.append(cloned);
      }.bind(this));
    } else {
      this.element_.html('');
    }

  }
};

/**
 * Directive for displaying notes for output plugins of a flow or hunt.
 *
 * @constructor
 * @ngInject
 * @export
 */
grrUi.outputPlugins.outputPluginNoteBodyDirective
    .OutputPluginNoteBodyDirective = function() {
  return {
    scope: {
      outputPlugin: '='
    },
    restrict: 'E',
    controller: OutputPluginNoteBodyController,
    controllerAs: 'controller'
  };
};

/**
 * Directive's name in Angular.
 *
 * @const
 * @export
 */
grrUi.outputPlugins.outputPluginNoteBodyDirective.OutputPluginNoteBodyDirective
    .directive_name = 'grrOutputPluginNoteBody';


});

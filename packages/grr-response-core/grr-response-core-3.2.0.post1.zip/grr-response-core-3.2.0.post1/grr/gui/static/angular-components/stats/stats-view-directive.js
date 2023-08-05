'use strict';

goog.provide('grrUi.stats.statsViewDirective.StatsViewController');
goog.provide('grrUi.stats.statsViewDirective.StatsViewDirective');

goog.scope(function() {

/**
 * Controller for StatsViewDirective.
 *
 * @param {!angular.Scope} $scope
 * @param {!grrUi.routing.routingService.RoutingService} grrRoutingService
 * @constructor
 * @ngInject
 */
grrUi.stats.statsViewDirective.StatsViewController = function(
    $scope, grrRoutingService) {
  /** @private {!angular.Scope} */
  this.scope_ = $scope;

  /** @private {!grrUi.routing.routingService.RoutingService} */
  this.grrRoutingService_ = grrRoutingService;

  /** @type {string} */
  this.selectionName;

  /** @type {number|null} */
  this.startTime;

  /** @type {number|null} */
  this.duration;

  /** @type {string|null} */
  this.clientLabel;

  /** @private {string} */
  this.oldSelectionName_;

  this.grrRoutingService_.uiOnParamsChanged(
      this.scope_,
      ['name', 'start_time', 'duration', 'client_label'],
      this.onUrlParamsChange_.bind(this));

  this.scope_.$watchGroup(
      ['controller.selectionName',
       'controller.startTime',
       'controller.duration',
       'controller.clientLabel'],
      this.onControllerParamsChange_.bind(this));
};
var StatsViewController =
    grrUi.stats.statsViewDirective.StatsViewController;


/**
 * Handles changes to the url parameters.
 *
 * @param {Array<string>} unused_values The param values.
 * @param {Object=} params The param dict.
 * @private
 */
StatsViewController.prototype.onUrlParamsChange_ = function(
    unused_values, params) {
  var selectionName = params['name'];
  if (angular.isDefined(selectionName)) {
    this.selectionName = selectionName;
  }

  var startTimeStr = params['start_time'];
  if (angular.isDefined(startTimeStr)) {
    this.startTime = parseInt(startTimeStr, 10);
  }

  var durationStr = params['duration'];
  if (angular.isDefined(durationStr)) {
    this.duration = parseInt(durationStr, 10);
  }

  var clientLabel = params['client_label'];
  if (angular.isDefined(clientLabel)) {
    this.clientLabel = clientLabel;
  }
};

/**
 * Handles changes to controller fields forwarded to reports as scope
 * parameters.
 *
 * @private
 */
StatsViewController.prototype.onControllerParamsChange_ = function() {
  if (angular.isUndefined(this.selectionName)) {
    return;
  }

  // Clear the report parameters on different report type selection.
  if (angular.isDefined(this.oldSelectionName_) &&
      this.oldSelectionName_ !== this.selectionName) {
    this.startTime = null;
    this.duration = null;
    this.clientLabel = null;
  }
  this.oldSelectionName_ = this.selectionName;

  var urlParams = {
    name: this.selectionName,
  };

  if (angular.isDefined(this.startTime)) {
    urlParams['start_time'] = this.startTime;
  }

  if (angular.isDefined(this.duration)) {
    urlParams['duration'] = this.duration;
  }

  if (angular.isDefined(this.clientLabel)) {
    urlParams['client_label'] = this.clientLabel;
  }

  this.grrRoutingService_.go('stats', urlParams);
};

/**
 * StatsViewDirective definition.
 *
 * @return {angular.Directive} Directive definition object.
 */
grrUi.stats.statsViewDirective.StatsViewDirective = function() {
  return {
    scope: {},
    restrict: 'E',
    templateUrl: '/static/angular-components/stats/stats-view.html',
    controller: StatsViewController,
    controllerAs: 'controller'
  };
};


/**
 * Name of the directive in Angular.
 *
 * @const
 * @export
 */
grrUi.stats.statsViewDirective.StatsViewDirective.directive_name =
    'grrStatsView';

});  // goog.scope

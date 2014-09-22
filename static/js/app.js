var app = angular.module('rmRemindMe',
  ['ui.bootstrap', 'rmUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', ['$scope', '$http', '$interval', '$timeout',
                             '$animate', 'rmL10n', 'rmTime',
  function rmSMSCtrl($scope, $http, $interval, $timeout, $animate, l10n, rmTime) {

  _scope = $scope;

  /** Init *******************************************************************/

  $scope.initSMS = function() {
    $scope.sms = {
      text: '',

      when: {
        day: new Date(),     // selected day
        time: new Date(),    // selected time

        // config
        minDate: new Date()  // only in the future
      }
    };
  };

  $scope.initSMS();

  // update each date to have only future ones everytime
  $scope.timeUpdater = $interval(function() {
    var nowPlusOneMinute = new Date(),
        when = $scope.sms.when;

    nowPlusOneMinute.setSeconds(0);
    nowPlusOneMinute.setMinutes(nowPlusOneMinute.getMinutes() + 1);

    if (when.day < nowPlusOneMinute) {
      when.day = nowPlusOneMinute;
      when.minDate = nowPlusOneMinute;
    }

    if (rmTime.sameDay(nowPlusOneMinute, when.day) &&
          when.time < nowPlusOneMinute) {
        when.time = nowPlusOneMinute;
      }
  }, 1000);

  /** Alerts *****************************************************************/

  $scope.alerts = [];
  $scope.closeAlert = function(alert) {
    var idx = $scope.alerts.indexOf(alert);
    if (idx < 0) { return; }
    $scope.alerts.splice(idx, 1);
  };
  $scope.addAlert = function(msg, typ) {
    var alert = {msg: msg, type: typ || 'warning'};
    $scope.alerts.push(alert);

    // hide alerts after 4sec
    $timeout(function() {
      $scope.closeAlert(alert);
    }, 4000);
  };

  /** Saving *****************************************************************/

  // returns the currently selected date as a string
  $scope.whenStr = function() {
    return rmTime.combineDateTime($scope.sms.when.day, $scope.sms.when.time)
                 .toUTCString();
  };


  $scope.scheduleSMS = function() {
    $http.post('/ajax/sms/schedule',
               {text: $scope.sms.text, when: $scope.whenStr()})
      .error(function(data) {
          $scope.addAlert(l10n.getString('server-error'), 'danger');
      })
      .success(function(data) {
          if (data.status) {
              $scope.addAlert(l10n.getString('success'), 'success');
              $scope.initSMS(); // clear the form
          } else {
              $scope.addAlert(l10n.getString('server-error'), 'danger');
          }
      });
  };
}]);

app.controller('rmSettingsCtrl', ['$scope', function rmSMSCtrl($scope) {
  // TODO
}]);

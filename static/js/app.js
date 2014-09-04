var app = angular.module('rmRemindMe', ['ui.bootstrap', 'rmUtils', 'mgo-mousetrap']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', ['$scope', '$http', '$interval', 'rmL10n', 'rmTime',
  function pcSMSCtrl($scope, $http, $interval, l10n, rmTime) {

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
    var nowPlusOneMinute = new Date();

    nowPlusOneMinute.setSeconds(0);
    nowPlusOneMinute.setMinutes(nowPlusOneMinute.getMinutes() + 1);

    $.each(['day', 'time', 'minDate'], function(_, field) {
      if ($scope.sms.when[field] < nowPlusOneMinute) {
          $scope.sms.when[field] = nowPlusOneMinute;
      }
    });
  }, 1000);

  /** Alerts *****************************************************************/

  $scope.alerts = [];
  $scope.closeAlert = function(idx) {
    $scope.alerts.splice(idx, 1);
  };
  $scope.addAlert = function(msg, typ) {
    $scope.alerts.push({msg: msg, type: typ || 'warning'});
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

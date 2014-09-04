var app = angular.module('rmRemindMe', ['ui.bootstrap', 'rmUtils']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', ['$scope', '$http', 'rmL10n', 'rmTime',
           function pcSMSCtrl($scope ,  $http ,    l10n ,  rmTime) {

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

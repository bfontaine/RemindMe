var app = angular.module('rmRemindMe',
  ['ui.bootstrap', 'rmUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', ['$scope', '$http', '$timeout', '$animate',
                             'rmL10n', 'rmTime',
  function rmSMSCtrl($scope, $http, $timeout, $animate, l10n, rmTime) {

  _scope = $scope; // debug

  /** Init *******************************************************************/

  $scope.initSMS = function() {
    var initialDate = new Date(),
        // initialize the date to now + 15 minutes
        initialMinutes = initialDate.getMinutes() + 15;

    // rounded to the next 5 multiple
    // e.g. 10 -> 15
    //      13 -> 15
    //      15 -> 20
    initialMinutes += 5 - initialMinutes % 5;

    initialDate.setMinutes(initialDate.getMinutes() + 15);

    $scope.sms = {
      text: '',

      when: {
        day: initialDate,     // selected day
        time: initialDate,    // selected time

        // config
        minDate: initialDate, // only in the future

        datePickerOpened: false
      }
    };
  };

  $scope.openDatePicker = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.sms.when.datePickerOpened = true;
  };

  $scope.initSMS();

  /** Alerts *****************************************************************/

  $scope.alerts = [];
  $scope.closeAlert = function(alert) {
    var idx = $scope.alerts.indexOf(alert);
    if (idx < 0) { return; }
    $scope.alerts.splice(idx, 1);
  };

  /*
    Examples:
      addAlert("my message");                // warning msg
      addAlert("my message", "info");        // info msg
      addAlert("my message", "info", 3000);  // fade 3s later
      addAlert("my message", "info", false); // don't fade
  */
  $scope.addAlert = function(msg, type_, timeout) {
    var alert = {msg: msg, type: type_ || 'warning'};
    $scope.alerts.push(alert);

    if (timeout !== false) {
      // hide alerts after 4sec
      $timeout(function() {
        $scope.closeAlert(alert);
      }, timeout || 4000);
    }
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

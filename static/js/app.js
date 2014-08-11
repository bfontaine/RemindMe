// localized strings retrieving from the DOM
var getString = (function() {
    var strs = {};

    $(function() {
        var lines = $('#_strings').html().split(/\n+/);
        $.each(lines, function(_, line) {
            var kv = line.split(/^([^:]+):/);
            if (kv) {
                strs[kv[1]] = kv[2];
            }
        });
    });

    return function(k) { return strs[k]; };
})();


var app = angular.module('rmRemindMe', ['ui.bootstrap']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', ['$scope', '$http',
                             function pcSMSCtrl($scope, $http) {

  $scope.text = '';
  $scope.when = {
    day: new Date(),     // selected day
    time: new Date(),    // selected time

    // config
    minDate: new Date()  // only in the future
  };

  // Alerts
  $scope.alerts = [];
  $scope.closeAlert = function(idx) {
    $scope.alerts.splice(idx, 1);
  };
  $scope.addAlert = function(msg, typ) {
    $scope.alerts.push({msg: msg, type: typ || 'warning'});
  };

  // returns the currently selected date as an ISO string
  $scope.whenStr = function() {
    var h = $scope.when.time.getHours(),
        m = $scope.when.time.getMinutes(),
        d = angular.copy($scope.when.day);

    d.setHours(h);
    d.setMinutes(m);

    // http://stackoverflow.com/a/16048201/735926
    d.setTime(d.getTime() - d.getTimezoneOffset()*60000);

    return d.toISOString();
  };


  $scope.scheduleSMS = function() {
    $http.post('/ajax/sms/schedule',
               {text: $scope.text, when: $scope.whenStr()})
      .error(function(data) {
          $scope.addAlert(getString('server-error'), 'danger');
      })
      .success(function(data) {
          if (data.status) {
              $scope.addAlert(getString('success'), 'success');
          } else {
              $scope.addAlert(getString('server-error'), 'danger');
          }
      });
  };
}]);

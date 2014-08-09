var app = angular.module('rmRemindMe', ['ui.bootstrap']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', function pcSMSCtrl($scope) {

  $scope.when = {
    day: null,           // selected day
    time: null,          // selected time

    // config
    minDate: new Date()  // only in the future
  };

  // returns the currently selected dateas an ISO string
  $scope.whenStr = function() {
    return 'TODO';
  };


  $scope.scheduleSMS = function() {
    // TODO

    console.log(w=$scope.when);
  };
});

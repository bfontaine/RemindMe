var app = angular.module('rmRemindMe', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('rmSMSCtrl', function pcSMSCtrl($scope) {

  // hard submit for now, see #12
  $scope.submitForm = function() { $('#sms-form').submit(); };

  // TODO
});

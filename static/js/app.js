var app = angular.module('pcRemindMe', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('pcSMSCtrl', function pcSMSCtrl($scope) {
  // TODO
});

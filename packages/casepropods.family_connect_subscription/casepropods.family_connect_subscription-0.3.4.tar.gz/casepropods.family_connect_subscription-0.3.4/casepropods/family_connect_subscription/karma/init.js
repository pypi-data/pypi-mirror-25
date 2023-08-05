angular.module('cases.directives', []);
angular.module('cases.controllers', []);
angular.module('cases', [
  'cases.directives',
  'cases.controllers'
])
.config(['$interpolateProvider', function ($interpolateProvider) {
  // Since Django uses {{ }}, we will have angular use [[ ]] instead.
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
}]);

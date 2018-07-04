app.directive('exSummary', [function () {
    return {
        restrict: 'E',
        scope: {
            item: "=",
            buy: "="
        },
        templateUrl: 'inc/sum.htm',
        controller: ["$scope", function ($scope) {
            // Isolated $scope here
        }]
    };
}])
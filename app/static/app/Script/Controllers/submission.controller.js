(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('SubmissionController',
        ['$scope', '$http', '$location', SubmissionController]);
    function SubmissionController($scope, $http, $location) {
        $scope.data = [];
        $scope.myRate = [];
        var urlParts =$location.absUrl().split('/');
        $http.get('/api/question_weight/' + urlParts[urlParts.length -2]).then(
            function (response) {
                $scope.data = response.data;
                console.log($scope.data);

            }, function (error) {
                console.log(error);
            }
        );
    }
})();
(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('ProgressController',
        ['$scope', '$http', '$location','$window', ProgressController]);
    function ProgressController($scope, $http, $location,$window) {
        $scope.submissions = [];
        var urlParts = $location.absUrl().split('/');
        $scope.type = urlParts[urlParts.length - 2];
        //urlParts[urlParts.length - 2] = 'IBM';
        $http.get('/api/submission/' + $scope.type ).then(
            function (response) {
                $scope.submissions = response.data;
                console.log($scope.submissions);

            }, function (error) {
                console.log(error);
            }
        );
        $scope.changeSelected = function () {
            $scope.selected = $scope.submissions[$scope.toSelect];
        };
        $scope.updateCandidate = function (option) {
            var toSend = {}
            toSend.user = $scope.selected.user.id;
            if (!!option) {
                switch(option)
                {
                    case 'Success':
                        toSend.option = 3;
                        break;
                    case 'Failed':
                        toSend.option = 4;
                        break;
                    default:
                        $('#updateSubmission').modal('hide');
                        return;
                }
            }
            $scope.selected = undefined;
            var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
             $http({
                method: 'POST',
                url: '/api/update/company/',
                data: toSend,
                headers: { "X-CSRFToken": $crf_token },
            }).then(
                 function (response) {
                     console.log($scope.submissions);
                     $('#updateSubmission').modal('hide');
                     $window.location.reload();
                 }, function (error) {
                     console.log(error);
                });
        }
    }
})();
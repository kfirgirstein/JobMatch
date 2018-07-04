(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('CProfileController',
        ['$scope', '$http', '$location', CProfileController]);
    function CProfileController($scope, $http, $location) {
        $scope.data = [];
        $scope.is_loading = true;
        $scope.toSend = [];
        $scope.candidates_number=1000
        var iteration = 0;
        $http.get('/api/question_weight/' + comps).then(
            function (response) {
                $scope.data = response.data;
                $scope.is_loading = false;
                console.log($scope.data);

            }, function (error) {
                console.log(error);
            }
        );
        $scope.startDemo = function () {
            var sum = 0.0;
            $scope.result_object = undefined;
            for (var i in $scope.toSend) {
                sum += parseFloat($scope.toSend[i]);
            }
            if (sum != 100) {
                $scope.error = true;
                return;
            }
            iteration++;
            $('#try_demo').modal('hide');
            $scope.is_loading = true;
            var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
            $http({
                method: 'POST',
                url: '/api/demo/',
                data: { 'imitate': $scope.toSend, 'iteration': iteration, 'candidates': parseInt($scope.candidates_number) },
                headers: { "X-CSRFToken": $crf_token },
            }).then(
                function (response) {
                    $scope.is_loading = false;
                    if (!!response.data) {
                        var parserd = JSON.parse(response.data);
                        $scope.result_object = parserd.Summary;
                        $('#result_modal').modal('show');
                        var new_weight = JSON.parse(parserd.Weight);
                        for (var i in $scope.data) {
                            $scope.data[i].weight = new_weight[i];
                        }
                    }
                }, function (error) {
                    console.log(error);
                });
        }
    }

})();
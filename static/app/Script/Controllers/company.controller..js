(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('CompanyController',
        ['$scope', '$http', '$location' , CompanyController]);
    function CompanyController($scope, $http, $location) {
        $scope.data = [];
        $scope.CompanyQuestions = [];
        $scope.is_loading = true;
        $scope.myChoice = 0;
        $http.get('/api/question/').then(
            function (response) {
                $scope.data = response.data;
                $scope.is_loading = false;
                console.log($scope.data);
            }, function (error) {
                console.log(error);
            }
        );
        $scope.showQuestionDetails = function () {
            $scope.selectedItem = undefined;
            if ($scope.myChoice > -1)
                $scope.selectedItem = Enumerable.From($scope.data)
                    .Where(function (x) { return x.id == $scope.myChoice })
                    .FirstOrDefault();
        };
        $scope.AddToList = function () {
            $scope.is_loading = true;
            if (!!$scope.selectedItem) {
                $scope.CompanyQuestions.push(angular.copy($scope.selectedItem))
                $scope.is_loading = false;
            }
            else {
                var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                $http({
                    url: '/api/add/question/',
                    method: "POST",
                    data: $scope.newItem,
                    headers: { "X-CSRFToken": $crf_token },
                }).then(
                    function (response) {
                        if (!!response.data) {
                            $scope.data = response.data;
                            $scope.CompanyQuestions.push($scope.data[$scope.data.length - 1]);
                            console.log($scope.data);
                            $scope.is_loading = false;
                        }
                    }, function (error) {
                        console.log(error);
                    }
                );
                $scope.newItem = undefined;
                $scope.numberOfQuestion = undefined;
            }
            $('#add_question').modal('hide')
        };
        $scope.submit = function () {
            var form = $("#myform").serializeArray();
            var questions_ids = $scope.selectedItem = Enumerable.From($scope.CompanyQuestions)
                .Select(function (x) { return x.id })
                .ToArray();
            form = form.concat([
                { name: "questions", value: JSON.stringify(questions_ids) },
            ]);

            $.post($location.absUrl(), form, function (d) {
                if (d.error) {
                    alert("There was a problem updating your user details")
                }
                window.location = "/home/";
            });
        };
    }
})();
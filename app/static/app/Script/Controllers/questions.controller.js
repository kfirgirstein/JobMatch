(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('QuestionController',
        ['$scope', '$http','$location' QuestionController]);
        function QuestionController($scope,$http,$location){
            $scope.data=[];
            $scope.myRate = [];
            var urlParts = $location.path().splite('/');
            $http.get('/api/questionsweight/' + urlParts[urlParts.length-1]).then(
                function(response)
                {
                    $scope.data=response.data;
                    console.log($scope.data);
                    
                },function(error)
                {
                    console.log(error);
                }
            );
            $scope.submit=function(){
              console.log($scope.myRate);
            };
        }
})();
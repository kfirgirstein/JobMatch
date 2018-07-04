(function () {
    'use strict';
    angular
        .module("JobMatch")
        .controller('LoginController',
        ['$scope', '$http','Login', LoginController]);
    function LoginController($scope, $http,Login) {
        $scope.login=function(){
            Login.login($scope.user).then(
                function(response)
                {
                    window.location = "/home/";
                },
                function(error)
                {
                    $scope.login_error = "Invalid username/password"
                }
            )
        }
       if (Login.isLoggedIn()){
           window.location = "/home/";
        }


    }
})();
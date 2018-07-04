(function () {
    'use strict';
    angular
        .module("JobMatch")
        .service('Login',
        ['$http', Login]);
    function Login($http) {
            this.login = login;
            this.getCurrentUser = getCurrentUser;
            this.isLoggedIn = isLoggedIn;
            this.logout = logout;
            this.redirectIfNotLoggedIn = redirectIfNotLoggedIn;
            function login(credentials){
                return $http({
                    method: 'POST',
                    url: '/auth_api/login/',
                    data: credentials,
                }).then(
                    function (response) {
                       localStorage.currentUser=JSON.stringify(response.data);
                    });
            };
            function isLoggedIn() {
                var flag= !!localStorage.currentUser;
                if(flag){
                $http.get('/auth_api/lslogin/').then(
                    function(response){
                        if (response.data==false)
                        delete localStorage.currentUser;
                    }
                )
                }
                return flag
            };
            function logout(){
                delete localStorage.currentUser;
                $http.get('/auth_api/logout/').then(
                    function(response){
                        window.location = "/login/";
                    },
                    function(error){
                        localStorage.login_error = "Error will logout" + error;
                    }                    
                )
                
            };
            function redirectIfNotLoggedIn(){
                if(!isLoggedIn()){
                    window.location = "/login/";
                }
            };
            function getCurrentUser()
            {
                return (!!localStorage.currentUser)?JSON.parse(localStorage.currentUser):null;
            }
    }
})();
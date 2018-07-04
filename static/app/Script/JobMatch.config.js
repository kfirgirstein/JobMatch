(function () {
    'use strict';
    angular.module('JobMatch')
        .run(['$http', run])
    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CRRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';   
    }
})();
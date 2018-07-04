(function () {
    'use strict'
    var app = angular.module('JobMatch', []);
    app.run(function ($rootScope, Login) {
        $rootScope.CurrentUser = Login.getCurrentUser();
        $rootScope.logout = Login.logout;
        $rootScope.searchCompany = function () {
            window.location = "/search/company/" + $rootScope.companyToSearch;
        };

    });
}());
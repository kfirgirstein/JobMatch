(function () {
    'use strict';
    angular
        .module("JobMatch")
        .directive('questionForm', QuestionFormDirective);
        function QuestionFormDirective(){
            return{
                templateUrl:'/static/app/Script/Templates/questionForm.template.html',
                restrict:'E'
            }
    }
        angular
            .module("JobMatch")
            .directive('questionBlank', QuestionBlankDirective);
        function QuestionBlankDirective($compile) {
            return {
                scope: {
                    selectedQuestion: '=',
                },
                templateUrl: '/static/app/Script/Templates/questionBlank.template.html',
                restrict: 'AE'
            }
        }

})();

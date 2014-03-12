'use strict';

angular.module('habeascorpus', [
    'ngRoute',
    'habeascorpus.controllers',
    'habeascorpus.directives',
]);

angular.module('d3', []);
angular.module('habeascorpus.controllers', []);
angular.module('habeascorpus.directives', ['d3']);

angular.module('habeascorpus')
    .config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
                when('/topics', {
                    templateUrl: 'partials/topic-list.html',
                    controller: 'TopicListController'
                }).
                when('/topics/:topicId', {
                    templateUrl: 'partials/topic-details.html',
                    controller: 'TopicDetailsController'
                });
        }]);

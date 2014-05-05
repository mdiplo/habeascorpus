'use strict';

angular.module('habeascorpus', [
    'ngRoute',
    'habeascorpus.controllers',
    'habeascorpus.directives',
    'habeascorpus.filters',
    'ui.bootstrap.pagination',
    'd3-angular'
]);

angular.module('habeascorpus.controllers', []);
angular.module('habeascorpus.directives', []);
angular.module('habeascorpus.filters', []);

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

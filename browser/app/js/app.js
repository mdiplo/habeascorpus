'use strict';

var habeascorpusApp = angular.module('habeascorpusApp', [
    'ngRoute',
    'habeascorpusControllers'
]);

habeascorpusApp.config(['$routeProvider',
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

'use strict';

var habeascorpusControllers = angular.module('habeascorpusControllers', []);

habeascorpusControllers.controller('TopicListController', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/api/topics/?format=json').success(function(data) {
            $scope.topics = data;
            console.log(data);
        }); 
    }]);

habeascorpusControllers.controller('TopicDetailsController', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        $scope.topicId = $routeParams.topicId;
    }]);
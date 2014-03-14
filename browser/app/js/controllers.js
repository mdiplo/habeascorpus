'use strict';

angular.module('habeascorpus.controllers')
    .controller('TopicListController', ['$scope', '$http',
        function ($scope, $http) {
            $http.get('/api/topics/?format=json').success(function(data) {
                $scope.topics = data;
            }); 
        }]);

angular.module('habeascorpus.controllers')
    .controller ('TopicDetailsController', ['$scope', '$routeParams', '$http',
        function($scope, $routeParams, $http) {
            $scope.topicId = $routeParams.topicId;
            
            $http.get('/api/topics/' + $routeParams['topicId'] + '?format=json')
                .success(function(data) {
                    $scope.topic = data;
                }); 

            $scope.loadDocuments = function(page) {
                $http.get('/api/topics/' + $routeParams['topicId'] + '/related_documents?page=' + page)
                .success(function(data) {
                    $scope.related_documents = data;
                    $scope.totalItems = data.count;
                });
            }

            //on charge la première page
            $scope.loadDocuments(1);
        }]);
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
            
            //charge les données générales du topic (id, related_words)
            $http.get('/api/topics/' + $routeParams['topicId'] + '?format=json')
                .success(function(data) {
                    $scope.topic = data;
                }); 
            
            //charge l'historique du topic pour afficher la courbe
            $http.get('/api/topics/' + $routeParams['topicId'] + '/history?format=json')
                .success(function(data) {
                    $scope.topic_history = data;
                });
            
            //charge les documents liés au topic
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

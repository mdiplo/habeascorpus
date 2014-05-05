'use strict';

angular.module('habeascorpus.controllers')
    .controller('TopicListController', ['$scope', '$http',
        function ($scope, $http) {
            $http.get('/api/topics/?format=json').success(function(data) {
                $scope.topics = data;
                $scope.topic_width = function (topic){
                    //renvoie la taille du topic en fonction de son poids
                    var max_weight = Math.max.apply(Math, data.map(function(o){ 
                        return o.weight_in_corpus;
                    }));
                    
                    var min_weight = Math.min.apply(Math, data.map(function(o){ 
                        return o.weight_in_corpus;
                    }));

                    var max_width = 100, // en pourcentage
                    min_width = 25;

                    return (max_width - min_width)/(max_weight - min_weight)*(topic.weight_in_corpus - max_weight) + max_width;

                }

                $scope.word_width = function(word, topic){
                    //renvoie la taille du mot en fonction de son poids dans le topic
                   
                    var total_words_weights = 0;
                    for(var i=0, n=topic.related_words.length; i<n; i++){
                        total_words_weights += topic.related_words[i].weight_in_topic;
                    }

                    return 100*word.weight_in_topic/total_words_weights;
                }

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

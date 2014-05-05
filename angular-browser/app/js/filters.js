'use strict';

/* Filters */

angular.module('habeascorpus.filters', [])

 .filter('capitalizeFirst', function() {
    return function(input, scope) {
        if (input != null){
            return input.substring(0, 1).toUpperCase()+input.substring(1);
        }
    }
 })
;


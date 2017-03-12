'use strict';

var scheduler = angular.module("scheduler", ["ngMaterial","smart-table"]);

angular
    .module('Application', [
        'appRoutes',
        'scheduler',
	    'ngResource',
    ]);

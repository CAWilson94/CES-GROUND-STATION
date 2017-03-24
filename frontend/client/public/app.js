'use strict';

var scheduler = angular.module("scheduler", ["ngMaterial","smart-table"]);

angular
    .module('Scheduler', [
        'appRoutes',
        'scheduler',
	    'ngResource',
    ]);

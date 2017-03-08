'use strict';

var scheduler = angular.module("scheduler", []);



angular
    .module('Application', [
        'appRoutes',
        'scheduler',
	    'ngResource',
	    'nya.bootstrap.select'
    ]);

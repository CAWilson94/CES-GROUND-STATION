'use strict';

var scheduler = angular.module("scheduler", ["ngMaterial"]);



angular
    .module('Application', [
        'appRoutes',
        'scheduler',
	    'ngResource',
    ]);

'use strict';

var scheduler = angular.module("scheduler", []);

angular
    .module('Scheduler', [
        'appRoutes',
        'scheduler',
	    'ngResource',
	    'ngMaterial'
    ]);

angular
	.module('ngMaterial',[
		'ng',
		'ngAnimate',
		'ngAria'])

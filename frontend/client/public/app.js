'use strict';

var scheduler = angular.module("scheduler", ["ngMaterial","smart-table"]);

angular
    .module('Scheduler', [
        'appRoutes',
        'scheduler',
	    'ngResource',
    ]);

angular
	.module('ngMaterial',[
		'ng',
		'ngAnimate',
		'ngAria'])

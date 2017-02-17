scheduler
	.controller('SchedulerController', function($scope, TLE){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
			$scope.message = "hello there ya tit";
		});
		
});


scheduler
	.controller('SchedulerController', function($scope, TLE){
		$scope.hello = "hello there ya tit";
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		
});


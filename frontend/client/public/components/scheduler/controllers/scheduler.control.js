scheduler
	.controller('SchedulerController', function($scope, TLE){
		$scope.hello = "hello tdddhere ya tit";

		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		
});


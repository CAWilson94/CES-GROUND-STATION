scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL,$timeout){

    $scope.tle = null;
    $scope.tles = null;
    $scope.loadSat = function() {

		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});

  };

		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});
   
  
     $scope.sizes = [
          "1: low",
          "2: default",
          "3: high",
      ];
		
    	
});








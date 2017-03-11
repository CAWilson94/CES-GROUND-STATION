scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL,$timeout){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});


		$scope.user = null;
  $scope.users = null;

  $scope.loadUsers = function() {

    $scope.users =  $scope.users  || [
        { id: 1, name: 'TEABAGS' },
        { id: 2, name: 'DOOPPYY' },
        { id: 3, name: 'BALALALLA' },
        { id: 4, name: 'ROASTERS' },
        { id: 5, name: 'CUBESAT1' },
        { id: 1, name: 'YERMAW' },
        { id: 2, name: 'LINDAAA' },
        { id: 3, name: 'BALDEEPSMAW' },
        { id: 4, name: 'COFFEE' },
        { id: 5, name: 'COOKIES' }
      ];
  };



    
		$scope.button_click = function() {
          window.alert("boopity");
      };

		
    	
});








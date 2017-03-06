scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL, $timeout){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});

		$scope.button_click = function() {
          window.alert("boopity");
      };
		
    	$('#tleTable').DataTable();	

    	 $timeout(function () {
    	 	$scope.$apply(function(){
    	 		 $('.selectpicker').parent().selectpicker({ showSubText:true});
    	 	})
                });
    	

    	
});


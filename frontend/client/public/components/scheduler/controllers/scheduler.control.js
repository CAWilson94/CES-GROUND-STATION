scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL,$timeout){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});

		
		$scope.button_click = function() {
          window.alert("boopity");
      };

		//$('.selectpicker').selectpicker('refresh');  


		/**
    	angular.element(document).ready(function(){
    		$('#tleTable').DataTable();	
  			//$('.selectpicker').selectpicker('refresh');   	
    	})
    	**/
    	
});


 scheduler.directive('bootSelectPicker', function() {
  return {
    restrict: "A",
    require: "ngModel",
    link: function(scope, element, attrs, ctrl) {
      setTimeout(function() {
       $(element).selectpicker('refresh');   
      }, 10);
     
    }
  };
})

 angular.element(function() {
  angular.bootstrap(document, ['scheduler']);
});






scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL){
		$scope.hello = "hello tdddhere ya tit";
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		// AZEL.query().$promise.then(function(date){
		// 	$scope.azel = data;
		// });
		
    	$('#tleTable').DataTable();	


   // angular
   // .module('sch', ['ngMaterial'])
   // .controller('AppCtrl', AppController);

    	var alert;
    	$scope.showAlert = showAlert;
    	$scope.showDialog = showDialog;
    	$scope.items = [1, 2, 3];

    	// Internal method
    	function showAlert() {
      		alert = $mdDialog.alert({
        	title: 'Attention',
        	textContent: 'This is an example of how easy dialogs can be!',
        	ok: 'Close'
      		});

       		$mdDialog
        	.show( alert )
        	.finally(function() {
          	alert = undefined;
        	});
    	}
	

});


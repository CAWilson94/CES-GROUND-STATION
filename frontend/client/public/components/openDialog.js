(function(angular, undefined){
  "use strict";

   // angular
   // .module('sch', ['ngMaterial'])
   // .controller('AppCtrl', AppController);
	function AppController($scope, $mdDialog) {
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
	}
})(angular);
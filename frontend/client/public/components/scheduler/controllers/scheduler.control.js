scheduler
  .controller('SchedulerController', function($scope, TLE, AZEL, $timeout) {

    $scope.tle = null;
    $scope.tles = null;
    // Loading required data into dropdown; can take a few ms

    $scope.loadSat = function() {
      // Grab TLE from Django 
      TLE.query().$promise.then(function(data) {
        $scope.tles = data;
      });
    };
    // Grabbing AZEL data from Django; under construction
    AZEL.query().$promise.then(function(date) {
      $scope.azel = data;
    });

    // priority settings for satellite scheduling
    $scope.priorities = [
      "1: low",
      "2: default",
      "3: high",
    ];

    // Dummy data for now; table update in construction
    $scope.rowCollection = [{
      firstName: 'Laurent',
      lastName: 'Renard',
      birthDate: new Date('1987-05-21'),
      balance: 102,
      email: 'whatever@gmail.com'
    }, {
      firstName: 'Blandine',
      lastName: 'Faivre',
      birthDate: new Date('1987-04-25'),
      balance: -2323.22,
      email: 'oufblandou@gmail.com'
    }, {
      firstName: 'Francoise',
      lastName: 'Frere',
      birthDate: new Date('1955-08-27'),
      balance: 42343,
      email: 'raymondef@gmail.com'
    }];

    // Should have updating sat pass object here..
    $scope.yermaw = [];
    $scope.hallo = "hello";
    // update table from drop down; will need to take in data from scheduler i.e. table dropdown --> fetch schedule data based on this then 
    // update table from scheduled data
    $scope.updateTable = function() {
      // can you send data from here to django model? Then update scope from the model?
      $scope.yermaw.push($scope.tle.name) // may have to replace with calling to another table for scheduler updates..
        //alert($scope.yermaw)
    };
  });
scheduler
  .controller('SchedulerController', function($scope, TLE, AZEL, $timeout, $http) {

    $scope.tle = null;
    $scope.tles = null;
    // Loading required data into dropdown; can take a few ms

    $scope.loadSat = function() {
      // Grab TLE from Django 
      TLE.query().$promise.then(function(data) {
        $scope.tles = data;
      });
    };

    $scope.loadAxel = function() {
      // Grabbing AZEL data from Django; under construction
      AZEL.query().$promise.then(function(date) {
        $scope.azel = data;
      });
    };

    $scope.priorities = [{
      name: "low",
      priority: 1,
    }, {
      name: "default",
      priority: 2,
    }, {
      name: "high",
      priority: 3,
    }];

    // Should have updating sat pass object here..
    $scope.name = [];
    $scope.pri = [];
    /**
     * SatMission object: sat name and priority
     * SatMissions List: containing sat missions objects
     */

    $scope.hallo = "hello";
    // update table from drop down; will need to take in data from scheduler i.e. table dropdown --> fetch schedule data based on this then 
    // update table from scheduled data

    var config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
      }
    }

    $scope.updateTable = function() {
      try {
        $scope.name.push($scope.tle.name)
        $scope.pri.push($scope.priority.priority)
        $http.post('http://127.0.0.1:8000/api/missions/', $scope.name).then(alert($scope.name))
      } catch (err) {
        alert("you must first select a satellite and a priority")
      }
    };

  });
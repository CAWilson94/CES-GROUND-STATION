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
    var missions

    $scope.hallo = "hello";
    // update table from drop down; will need to take in data from scheduler i.e. table dropdown --> fetch schedule data based on this then 
    // update table from scheduled data

    var config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
      }
    }

    /**
     * Take in current clicked dropdown inputs: sat name and priority.
     * Pass these to back end to add to current missions. 
     * @return void 
     */
    $scope.updateTable = function() {
      try {
        // Try for select input AND POST 
        $scope.name.push($scope.tle.name)
        $scope.pri.push($scope.priority.priority)

        try {
          // Not sure this try should be here, try for post 

          $http.post('http://127.0.0.1:8000/api/missions/', $scope.name)
            .then(function successCallBack(response) {
                // Succeess is anything between 200 and 299
                console.log("yasss")
              },
              function errorCallBack(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                // Error is anything outside of range previously mentioned. 
                console.log(response.status + " : " + response.statusText);
              });

        } catch (err) {
          console.log("Post went wrong..")
        }

      } catch (err) {
        alert("you must first select a satellite and a priority")
      }



    };



  });
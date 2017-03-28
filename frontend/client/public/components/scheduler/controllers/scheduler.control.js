scheduler
  .controller('SchedulerController', function($scope, TLE, AZEL, Mission, $timeout, $http) {

    $scope.tle = null;
    $scope.tles = null;

    $scope.nextpass = null;
    $scope.nextpasses = null;

    /**
     * Load in TLE data from Django side
     * @return {[type]} [description]
     */
    $scope.loadSat = function() {
      // Grab TLE from Django 
      TLE.query().$promise.then(function(data) {
        $scope.tles = data;
      });
    };

    /**
     * Load in azimuth and elevation values from Django Models
     */
    $scope.loadAxel = function() {
      // Grabbing AZEL data from Django; under construction
      AZEL.query().$promise.then(function(data) {
        $scope.azel = data;
      });
    };

    /**
     * Download csv from current next pass tables
     */
    $scope.downloadCSV = function() {

      $http({
        method: 'GET',
        url: 'http://localhost:8000/api/csv/missions',
        headers: {
          'Content-Type': 'text/csv'
        },
      }).then(function successCallback(response) {
        // this callback will be called asynchronously
        // when the response is available
        window.location.href = ('http://localhost:8000/api/csv/missions')
        console.log(response)
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
    };



    /**
     * TODO: next passes model in here: the service for this does not have the right URL as the URL is not made yet
     * @return void
     */
    $scope.loadNextPasses = function() {

      var config = {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }

      $http.get('http://127.0.0.1:8000/api/schedulemissiontest', config)
        .then(function successCallback(response, data) {
          // this callback will be called asynchronously
          // when the response is available
          $scope.nextpasses = response.data;
          console.log($scope.nextpass)

        }, function errorCallback(response) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
          console.log("NUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        });
    }


    $scope.loadNextPasses()

    /**
     * priorities: should default at 2 in dropdown 
     * @type {Array}
     */
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

    /**
     * SatMission object: sat name and priority
     * SatMissions List: containing sat missions objects
     */

    // update table from drop down; will need to take in data from scheduler i.e. table dropdown --> fetch schedule data based on this then 
    // update table from scheduled data


    /**
     * Take in current clicked dropdown inputs: sat name and priority.
     * Pass these to back end to add to current missions. 
     * @return void 
     */
    $scope.updateTable = function() {

      $scope.loadNextPasses();
      // Each mission requires a sat name and a priority

      $scope.mission = {
        name: $scope.tle.name,
        priority: $scope.priority.priority
      };


      try {
        console.log($scope.mission)
          // Not sure this try should be here, try for post 
        $http.post('http://127.0.0.1:8000/api/save/mission/', $scope.mission)
          .then(function successCallBack(response) {
              // Succeess is anything between 200 and 299
              $scope.missions = Mission.get().$promise.then(function(data) {
                $scope.missions = data;
              });

              console.log(response)
            },
            function errorCallBack(response) {
              // called asynchronously if an error occurs
              // or server returns response with an error status.
              // Error is anything outside of range previously mentioned. 
              console.log(response.status + " : " + response.statusText);
            }
            // Uncomment for testing output or use django shell to check missions model contents
            //alert($scope.mission.name + " : " + $scope.mission.priority)
          );
      } catch (err) {
        alert("you must first select a satellite and a priority")
      }


    };


    /**
     *
     * while there is nothing populating the table: show output as animation loader
     * 
     */



    //MISSSION TABLE

    $scope.missions = Mission.get().$promise.then(function(data) {
      $scope.missions = data;
    });

    $scope.deleteMission = function(mission) {
      id = mission.id;
      Mission.delete({
        id: id
      }, (function(resp) {
        console.log(resp);
        removeA($scope.missions, mission)
      }))

    };

    function removeA(arr) {
      //What is this?!
      var what, a = arguments,
        L = a.length,
        ax;
      while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax = arr.indexOf(what)) !== -1) {
          arr.splice(ax, 1);
        }
      }
      return arr;
    }


    // End of controller please leave it alone.
  });
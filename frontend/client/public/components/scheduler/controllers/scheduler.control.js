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
    // Grabbing AZEL data from Django; under construction
     $scope.getAzel = function(){
      AZEL.query().$promise.then(function(date) {
      $scope.azel = data;
    });



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
    $scope.name = [];
    $scope.hallo = "hello";
    // update table from drop down; will need to take in data from scheduler i.e. table dropdown --> fetch schedule data based on this then 
    // update table from scheduled data
    // 
    // 
    var config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
      }
    }


    $scope.buttonClick = function() {
      alert("something was clicked")
    }

    $scope.updateTable = function() {
      try {

        $scope.name.push($scope.tle.name)
        $http.post('http://127.0.0.1:8000/api/missions/', $scope.name).then(alert($scope.name))

      } catch (err) {
        alert("you must first select a satellite and a priority")
      }



      // passed name to server: should schedule then update the next pass list which we want to pull in ... aye. 
    };
    /**
      .$promise.catch(function(response) {
        console.log($scope.name)
          //this will be fired upon error
        if (response.status == 500) alert('Something baaad happend');
      })
      */



    /*
     * Comms with server side: http for post request
     *
    .factory('satsFactory', ['$http', function($http) {
      return function name() {
        var fac = {};
        // obvious naming is obvious: will change later
        fac.addChosenSatToDB = function() {
          $http.post("localhost:8000/api/postmission/")
        }
        return fac;
      };
    }]) */


    /**
     *
     *<..ng-app="app"
    // Instead of button: select picker .. forgot what I wrote for it. 
    <input type="button" ng-click="app.addSatClicked(app.satClicked)"/>

    ..controller:

    app.addSatClicked = function (satClicked){
      $http.post("http://someurl", satClicked){  ** what url? could we replace with something else? ** 
        .success(function(data){
          app.people = data;
        })
      })

    }
      
      
      
      
      ------------------>
    app.post(...function(req, res){
      data.push(req.body);
      res.send(data)
     *
     *
     * 
     */

  });
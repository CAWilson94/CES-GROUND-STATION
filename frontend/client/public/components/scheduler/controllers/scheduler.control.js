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
    // 
    // 
    var config = {
                headers : {
                    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                }
            }

    $scope.updateTable = function() {
      // can you send data from here to django model? Then update scope from the model?
      $scope.yermaw.push($scope.tle.name) // may have to replace with calling to another table for scheduler updates..
      var bob = "bob"
      $http.post('localhost:8000/api/postmission/', $scope.yermaw, config)
      .success(alert($scope.yermaw + " yasss " + bob))
      .error(alert("nuuuuuuuuu"));
    };

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
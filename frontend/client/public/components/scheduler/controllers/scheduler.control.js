scheduler
    .controller('SchedulerController', function ($scope, TLE, AZEL, Mission, $timeout, $http) {

        $scope.tle = null;
        $scope.tles = null;

        /**
         * Load in TLE data from Django side
         * @return {[type]} [description]
         */
        $scope.loadSat = function () {
            // Grab TLE from Django
            TLE.query().$promise.then(function (data) {
                $scope.tles = data;
            });
        };

        /**
         * Load in azimuth and elevation values from Django Models
         */
        $scope.loadAxel = function () {
            // Grabbing AZEL data from Django; under construction
            AZEL.query().$promise.then(function (date) {
                $scope.azel = data;
            });
        };

        // priorities: should default at 2 in dropdown

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

        // Not in use currently: should default to JSON but in case we need them?
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
        $scope.updateTable = function () {


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
                        $scope.missions = Mission.get().$promise.then(function (data) {
                            $scope.missions = data;
                        });
                        console.log(response)
                    },
                    function errorCallBack(response) {
                        // called asynchronously if an error occurs
                        // or server returns response with an error status.
                        // Error is anything outside of range previously mentioned.
                        console.log(response.status + " : " + response.statusText);
                    },
                    // Uncomment for testing output or use django shell to check missions model contents
                    alert($scope.mission.name + " : " + $scope.mission.priority)
                );
            } catch (err) {
                alert("you must first select a satellite and a priority")
            }

        };

        //MISSSION TABLE
        $scope.missions = Mission.get().$promise.then(function (data) {
            $scope.missions = data;
        });

        $scope.deleteMission = function (mission) {
            id = mission.id;
            Mission.delete({id: id}, (function (resp) {
                console.log(resp);
                removeA($scope.missions, mission)
            }))

        };

        function removeA(arr) {
            //What the fuck is this?!
            var what, a = arguments, L = a.length, ax;
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
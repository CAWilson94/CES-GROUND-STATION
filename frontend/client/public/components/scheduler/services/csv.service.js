scheduler
    .factory('CSV', function($resource) {
        return $resource(
            'http://localhost:8000/api/csv/missions', // CHANGE TO NEXT PASS
            {
                get: {
                    method: 'GET',
                    isArray: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                },
            }, {
                stripTrailingSlashes: false
            }
        );
    });
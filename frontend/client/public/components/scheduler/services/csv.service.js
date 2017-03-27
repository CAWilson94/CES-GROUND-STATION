scheduler
    .factory('CSV', function($resource) {
        return $resource(
            'http://localhost:8000/api/csv/missions', // CHANGE TO NEXT PASS
            {
                get: {
                    method: 'GET',
                    isArray: false,
                    headers: {
                        'Content-Type': 'text/csv',
                        'Accept': 'text/csv'
                    }
                },
            }, {
                stripTrailingSlashes: false
            }
        );
    });
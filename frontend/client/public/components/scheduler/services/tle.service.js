scheduler
    .factory('TLE', function($resource) {
        return $resource(
            'http://localhost:8000/api/tles/:id/',
            {},
            {
                query: {
                    method: 'GET',
                    isArray: true,
                    headers: {
                        'Content-Type':'application/json',
                        'Accept':'application/json'
                    }
                }
            },
            {
                stripTrailingSlashes: false
            }
        );
    });
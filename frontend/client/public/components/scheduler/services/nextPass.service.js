scheduler
    .factory('NextPass', function($resource) {
        return $resource(
            'http://localhost:8000/api/tles/:id/', // WHATEVER URL SHOULD BE HERE 
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
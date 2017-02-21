scheduler
    .factory('AZEL',function($resource) {
        return $resource(
            'http://localhost:8000/api/tles/:id/azel',
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
scheduler
    .factory('Mission', function ($resource) {
        return $resource(
            'http://localhost:8000/api/missions/:id/',
            {id: '@id'},
            {
                get: {
                    method: 'GET',
                    isArray: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                },
                delete: {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                }
                //post:{
                //    method: 'POST',
                //    headers: {
                //        'Content-Type': 'application/json',
                //        'Accept': 'application/json'
                //    }
                //}
            },
            {
                stripTrailingSlashes: false
            }
        );
    });
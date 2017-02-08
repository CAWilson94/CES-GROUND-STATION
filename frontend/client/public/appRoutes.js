angular
    .module('appRoutes', ["ui.router"])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    $stateProvider.state({
        name: 'scheduler',
        url: '/',
        templateUrl: 'public/components/scheduler/templates/scheduler.template.html',
        controller: 'SchedulerController'
    });

    $urlRouterProvider.otherwise('/');
}]);

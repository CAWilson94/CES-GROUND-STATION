/*
	Assigning maincontroller called "MainController" to the MyTutorial
	App application.

	Assign all controller variables in the $scope funtion param
	which will make them available within the #content div in the html 
	page

	The scope is available only to the controller so you could not access
	the variable from outside the #content div
	unless the same controller was defined


	----DATA BINDING ----
	Example: declare a scope object to act as a model 
	inputValue

*/

app.controller("MainController", function($scope){
  $scope.selectedPerson = 0;
  $scope.selectedGenre = null;
  $scope.hello = "hello yer mawww";
  $scope.people = [
    { id: 0, name: 'Leon', music: [ 'Rock', 'Metal', 'Dubstep', 'Electro' ] },
    { id: 1, name: 'Chris', music: [ 'Indie', 'Drumstep', 'Dubstep', 'Electro' ] },
    { id: 2, name: 'Harry', music: [ 'Rock', 'Metal', 'Thrash Metal', 'Heavy Metal' ] },
    { id: 3, name: 'Allyce', music: [ 'Pop', 'RnB', 'Hip Hop' ] }
  ];
});
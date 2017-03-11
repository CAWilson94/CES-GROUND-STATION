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
  $scope.sizes = [
          "small (12-inch)",
          "medium (14-inch)",
          "large (16-inch)",
          "insane (42-inch)"
      ];
   $scope.toppings = [
        { category: 'meat', name: 'Pepperoni' },
        { category: 'meat', name: 'Sausage' },
        { category: 'meat', name: 'Ground Beef' },
        { category: 'meat', name: 'Bacon' },
        { category: 'veg', name: 'Mushrooms' },
        { category: 'veg', name: 'Onion' },
        { category: 'veg', name: 'Green Pepper' },
        { category: 'veg', name: 'Green Olives' }
      ];
    $scope.selectedToppings = [];
    $scope.printSelectedToppings = function printSelectedToppings() {
        var numberOfToppings = this.selectedToppings.length;

        // If there is more than one topping, we add an 'and'
        // to be gramatically correct. If there are 3+ toppings
        // we also add an oxford comma.
        if (numberOfToppings > 1) {
          var needsOxfordComma = numberOfToppings > 2;
          var lastToppingConjunction = (needsOxfordComma ? ',' : '') + ' and ';
          var lastTopping = lastToppingConjunction +
              this.selectedToppings[this.selectedToppings.length - 1];
          return this.selectedToppings.slice(0, -1).join(', ') + lastTopping;
        }

        return this.selectedToppings.join('');
      };
});
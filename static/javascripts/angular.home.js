/**
 * Created by sean on 15. 10. 2.
 */

var myApp = angular.module('pageHomeApp',[]);

myApp.factory("items", function (data) {
/*    $http.get('/DocumentsList').success(function(data){
        d.resolve(data);
    });*/
    var items = {};
    items.data = [{
        id: "1",
        title: "Item 1",
        brand: "NongSim",
        content: "Contents here"
    }, {
        id: "2",
        title: "Item 2",
        brand: "Samyang",
        content: "Contents here"
    }, {
        id: "3",
        title: "Item 3",
        brand: "HaiTai",
        content: "Contents here"
    }, {
        id: "4",
        title: "Item 4",
        brand: "Gold",
        content: "Contents here"
    }];
    return items;
});

function ItemsController($scope, items, $http) {
    $scope.items = items;

    $scope.openDetail = function($window, id) {

        $scope.content = 'http://localhost:8880/single-page.html';
        $http.get('http://localhost:8880/single-page.html',
            {
                params: { id: id }
            });
        //$window.location = "http://localhost:8880/single-page.html";
    }


/*    $scope.deleteItem = function (index) {
        items.data.splice(index, 1);
    }
    $scope.addItem = function (index) {
        items.data.push({
            id: $scope.items.data.length + 1,
            title: $scope.newItemName
        });
    }*/
}
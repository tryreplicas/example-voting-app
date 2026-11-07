var app = angular.module('catsvsdogs', []);
var socket = io.connect();

var bg1 = document.getElementById('background-stats-1');
var bg2 = document.getElementById('background-stats-2');

app.controller('statsCtrl', function($scope){
  $scope.aPercent = 50;
  $scope.bPercent = 50;

  var updateScores = function(){
    socket.on('scores', function (json) {
       data = JSON.parse(json);
       var a = parseInt(data.a || 0);
       var b = parseInt(data.b || 0);

       var percentages = getPercentages(a, b);

       bg1.style.width = percentages.a + "%";
       bg2.style.width = percentages.b + "%";

       $scope.$apply(function () {
         $scope.aPercent = percentages.a;
         $scope.bPercent = percentages.b;
         $scope.total = a + b;
       });
    });
  };

  var init = function(){
    document.body.style.opacity=1;
    updateScores();
  };
  socket.on('message',function(data){
    init();
  });
});

// Rounding rule for each share's base value. Swap Math.round for Math.ceil
// (or Math.floor) here to change semantics; largestRemainder keeps the sum at 100.
function roundShare(value) {
  return Math.round(value);
}

// Whole-number percentages that always sum to exactly 100 (largest-remainder
// method): round each share, then add/remove the leftover points one at a time
// from the shares whose rounding moved them furthest from their exact value.
function largestRemainder(counts) {
  var total = counts.reduce(function (sum, n) { return sum + n; }, 0);
  if (total <= 0) {
    // No votes yet: split evenly (50/50 for two options).
    counts = counts.map(function () { return 1; });
    total = counts.length;
  }

  var exact = counts.map(function (n) { return n / total * 100; });
  var rounded = exact.map(roundShare);
  var diff = 100 - rounded.reduce(function (sum, n) { return sum + n; }, 0);
  var step = diff > 0 ? 1 : -1;

  // Indices ordered by how much each share is owed (or over-allocated).
  var order = exact.map(function (_, i) { return i; }).sort(function (i, j) {
    return step * ((exact[j] - rounded[j]) - (exact[i] - rounded[i]));
  });

  for (var k = 0; diff !== 0; k = (k + 1) % order.length) {
    rounded[order[k]] += step;
    diff -= step;
  }

  return rounded;
}

function getPercentages(a, b) {
  var shares = largestRemainder([a, b]);
  return { a: shares[0], b: shares[1] };
}

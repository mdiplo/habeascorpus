angular.module('d3-angular', [])
  .directive('lineChart', ['d3Service', function(d3Service) {
      return {
          restrict: 'EA',
          scope: {
              data: '=' // bi-directional data-binding
          },

          link: function(scope, element, attrs) {

              var svg = d3.select(element[0])
              .append("svg")

              scope.$watch('data', function(newVals, oldVals) {
                  return scope.render(newVals);
              }, true);

              scope.render = function(data){

                  if (!data) return;

                  var width = 720,
                  height = 300;

                  var parseDate = d3.time.format("%Y").parse;
                  
                  data.forEach(function(d) {
                      d.date = parseDate(String(d.date));
                      d.year = d.date.getFullYear();
                  });  

                  
                  var x = d3.time.scale()
                      .range([0, width]);

                  var y = d3.scale.linear()
                      .range([height, 0]);
                  
                  var xAxis = d3.svg.axis()
                      .scale(x)
                      .orient("bottom");

                  var yAxis = d3.svg.axis()
                      .scale(y)
                      .orient("left");
                  
                  var line = d3.svg.line()
                      .interpolate("cardinal")
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y(d.value); });
                  
                  x.domain(d3.extent(data, function(d) { return d.date; }));
                  y.domain(d3.extent(data, function(d) { return d.value; }));

                  svg.attr("width", width + margin.left + margin.right)
                      .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
                  
                  svg.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis);
                  
                  svg.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  
                  svg.append("path")
                  .datum(data)
                  .attr("class", "line")
                  .attr("d", line);

                  svg.append("g")
                      .selectAll('circle')
                      .data(data)
                     .enter()
                      .append('circle')
                      .attr('cx', function (d) { return x(d.date); })
                      .attr('cy', function (d) { return y(d.value); })
                      .attr('r', 4)
                      .attr('class', 'curvepoints')

                    }
            }
        }
    }]);

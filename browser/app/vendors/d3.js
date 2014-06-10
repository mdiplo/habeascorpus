angular.module('d3-angular', [])
  .directive('lineChart', function() {
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

                  var  margin = {'left': 50, 'right': 20, 'top': 10, 'bottom': 20},
                    width = 800,
                    height = 300,
                    xName = 'key',
                    yName = 'value',
                    getX = function (d){ return d[xName.toString()]; }
                    getY = function (d){ return d[yName.toString()]; }
                  ;
                 

                  var parseDate = d3.time.format("%Y").parse;
                  
                  var x = d3.time.scale()
                      .range([0, width]);

                  var y = d3.scale.linear()
                      .range([height, 0]);
                  
                  var xAxis = d3.svg.axis()
			.tickFormat(d3.format("04d"))
                      .scale(x)
                      .orient("bottom");

                  var yAxis = d3.svg.axis()
                      .scale(y)
                      .orient("left");
                  
                  var line = d3.svg.line()
                      .interpolate("cardinal")
                      .x(function(d) { return x(getX(d)); })
                      .y(function(d) { return y(getY(d)); });
                  
                  x.domain(d3.extent(data, function(d) { return getX(d); }));
                  y.domain(d3.extent(data, function(d) { return getY(d); }));

                  svg = svg.attr("width", width + margin.left + margin.right)
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
                      .attr('cx', function (d) { return x(d.key); })
                      .attr('cy', function (d) { return y(d.value); })
                      .attr('r', 4)
                      .attr('class', 'curvepoints')

                    }
            }
        }
    });

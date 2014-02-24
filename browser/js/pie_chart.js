function pieChart() {
    
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 200,
    height = 200,
    radius = Math.min(width, height) / 2;
    
    get_name = function(d) { return d.word; }
    get_value = function(d) { return d.topic_score; }
    
    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    
    var arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);
    
    var pie = d3.layout.pie()
    .sort(null)
    .value(get_value);

    function chart(selection) {
        selection.each(function(data) {
           
            var svg = d3.select(this).append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
            
            var g = svg.selectAll(".arc")
            .data(pie(data))
          .enter().append("g")
            .attr("class", "arc");
              
            g.append("path")
            .attr("d", arc)
            .style("fill", function(d) { return color(d.data.word);});
 
            g.append("text")
            .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
            .attr("dy", ".35em")
            .style("text-anchor", "middle")
            .text(function (d) { return d.data.word;})
        });
    }

    
    chart.width = function(value) {
        if (!arguments.length) return width;
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) return height;
        height = value;
        return chart;
    };
    
    chart.get_name = function(f){ 
        get_name = f;
    }
    
    chart.get_value = function(f)
        get_value = f;
    
    return chart;
}